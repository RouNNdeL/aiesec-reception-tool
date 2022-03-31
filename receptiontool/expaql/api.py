from __future__ import annotations

import base64
from datetime import datetime, timedelta
from http import HTTPStatus
import logging
from typing import Any, Callable, List, Optional

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from pydantic import BaseModel
from pydantic.class_validators import validator
import requests
from requests.exceptions import JSONDecodeError

from .models import CurrentPerson, GqlSchema, OpportunityApplication

EXPA_GRAPHQL_URL = "https://gis-api.aiesec.org/graphql"


class ExpaAuthException(Exception):
    pass


class ExpaUnknwonException(Exception):
    pass


class TokenRefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    created_at: datetime

    @validator("created_at", pre=True)
    def parse_created_at(cls: Any, v: Any) -> datetime:
        assert isinstance(v, int)

        return datetime.fromtimestamp(v)

    def expires_at(self) -> datetime:
        return self.created_at + timedelta(self.expires_in)


class ExpaQuery:
    __gql_client: Client
    __token_expire: datetime
    __client_id: str
    __client_secret: str
    refresh_token_callback: Optional[Callable[[str], None]]

    @property
    def __refresh_token(self) -> str:
        return self.___refresh_token

    @__refresh_token.setter
    def __refresh_token(self, value: str) -> None:
        self.___refresh_token = value
        logging.debug("Settings new token")
        if self.refresh_token_callback is not None:
            self.refresh_token_callback(value)

    @__refresh_token.deleter
    def __refresh_token(self) -> None:
        del self.___refresh_token

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        initial_refresh_token: str,
        refresh_token_callback: Optional[Callable[[str], None]] = None,
    ):
        token_len = len(initial_refresh_token)
        if token_len != 64:
            raise ValueError(f"Invalid token length, expected 64 got {token_len}")

        client_id_len = len(client_id)
        if client_id_len != 64:
            raise ValueError(
                f"Invalid client_id length, expected 64 got {client_id_len}"
            )

        client_secret_len = len(client_secret)
        if client_secret_len != 64:
            raise ValueError(
                "Invalid client_secret length, expected 64 got {client_secret_len}"
            )

        self.refresh_token_callback = refresh_token_callback
        self.__refresh_token = initial_refresh_token
        self.__client_id = client_id
        self.__client_secret = client_secret

        token = self.__do_refresh_token()
        self.__init_client(token)

    def __init_client(self, token: str) -> None:
        transport = RequestsHTTPTransport(
            url=EXPA_GRAPHQL_URL, headers={"Authorization": token}
        )
        self.__gql_client = Client(transport=transport)

    def __check_token(self) -> None:
        if datetime.now() >= self.__token_expire:
            token = self.__do_refresh_token()
            self.__init_client(token)

    def __do_refresh_token(self) -> str:
        auth = base64.b64encode(
            f"{self.__client_id}:{self.__client_secret}".encode()
        ).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "refresh_token": self.__refresh_token,
            "grant_type": "refresh_token",
        }

        response = requests.post(
            "https://auth.aiesec.org/oauth/token", headers=headers, data=data
        )
        try:
            json = response.json()
        except JSONDecodeError as e:
            raise ExpaUnknwonException(e)

        if (
            response.status_code == HTTPStatus.UNAUTHORIZED
            and "error_description" in json
        ):
            raise ExpaAuthException(f"Unauthorized: {json['error_description']}")
        elif response.status_code != 200:
            raise ExpaUnknwonException(
                f"Invalid status code {response.status_code}:"
                f"{response.content.decode()}"
            )

        token_response = TokenRefreshResponse(**json)
        self.__refresh_token = token_response.refresh_token
        self.__token_expire = token_response.expires_at()

        return token_response.access_token

    def get_refresh_token(self) -> str:
        return self.__refresh_token

    def get_current_person(self) -> CurrentPerson:
        self.__check_token()

        query = gql(
            """
            query ProfileQuery {
              currentPerson {
              """
            + CurrentPerson.get_query()
            + """
              }
            }
        """
        )

        return CurrentPerson(**self.__gql_client.execute(query)["currentPerson"])

    def get_applications(self) -> List[OpportunityApplication]:
        self.__check_token()

        query = gql(
            """
            query ApplicationsQuery {
              allOpportunityApplication {
                ...ApplicationList
                __typename
              }
            }

            fragment ApplicationList on OpportunityApplicationList {
                data {
                      """
            + OpportunityApplication.get_query()
            + """
                }
            }
        """
        )

        return [
            OpportunityApplication(**it)
            for it in self.__gql_client.execute(query)["allOpportunityApplication"][
                "data"
            ]
        ]

    def get_applications_by_ids(self, ids: List[int]) -> List[OpportunityApplication]:
        self.__check_token()

        return [it for it in self.get_applications() if it.opportunity.id in ids]

    def get_schema(self, typename: str) -> GqlSchema:
        self.__check_token()

        query = gql(
            """
            {
              __type(name: """
            + f'"{typename}"'
            + """) {
                name
                fields {
                  name
                  type {
                    name
                    kind
                  }
                }
              }
            }
        """
        )

        d = self.__gql_client.execute(query)["__type"]
        return GqlSchema(**d)

    def get_enum_values(self, typename: str) -> List[str]:
        self.__check_token()

        query = gql(
            """
            {
              __type(name: """
            + f'"{typename}"'
            + """) {
                    enumValues {
                          name
                    }
                }
            }
            """
        )

        return [
            it["name"]
            for it in self.__gql_client.execute(query)["__type"]["enumValues"]
        ]
