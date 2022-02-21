# create a class that will wrap graphql queries for AIESEC EXPA platform

from __future__ import annotations
from typing import Dict

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.async_transport import AsyncTransport
from gql.transport.transport import Transport

from .models import CurrentPerson


EXPA_GRAPHQL_URL = "https://gis-api.aiesec.org/graphql"


class ExpaQuery:
    transport: Transport | AsyncTransport
    client: Client

    def __init__(self, initial_token: str):
        self.transport = AIOHTTPTransport(
            url=EXPA_GRAPHQL_URL, headers={"Authorization": initial_token}
        )
        self.client = Client(transport=self.transport)

    def get_current_person(self):
        query = gql(
            """
            query ProfileQuery {
              currentPerson {
              """ + CurrentPerson.get_query() + """
              }
            }
        """
        )

        return CurrentPerson.from_dict(self.client.execute(query)["currentPerson"])

    def get_schema(self, typename: str) -> Dict[str, Dict[str, str]]:
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

        return self.client.execute(query)["__type"]
