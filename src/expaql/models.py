from __future__ import annotations
from typing import Dict
from abc import ABC

from datetime import datetime
from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class ExpaModel(ABC):
    @staticmethod
    def from_dict(d: Dict) -> ExpaModel | None:
        if d["__typename"] == "CurrentPerson":
            return CurrentPerson.from_dict(d)
        elif d["__typename"] == "Office":
            return Office.from_dict(d)
        else:
            return None


class CurrentPerson(ExpaModel):
    id: int
    aiesec_email: str
    cover_photo: str
    created_at: datetime
    current_office: Office
    email: str
    full_name: str
    gender: Gender

    def __init__(
        self,
        id: int,
        aiesec_email: str,
        cover_photo: str,
        created_at: datetime,
        current_office: Office,
        email: str,
        full_name: str,
        gender: Gender,
    ):
        super().__init__()
        self.id = id
        self.aiesec_email = aiesec_email
        self.cover_photo = cover_photo
        self.created_at = created_at
        self.current_office = current_office
        self.email = email
        self.full_name = full_name
        self.gender = gender

    def __str__(self) -> str:
        return f"{self.full_name} from {self.current_office}"

    @staticmethod
    def from_dict(d: Dict) -> CurrentPerson:
        return CurrentPerson(
            d["id"],
            d["aiesec_email"],
            d["cover_photo"],
            d["created_at"],
            Office.from_dict(d["current_office"]),
            d["email"],
            d["full_name"],
            Gender(d["gender"]),
        )

    @staticmethod
    def get_query() -> str:
        return (
            """
            id
            aiesec_email
            cover_photo
            created_at
            current_office {
                """
            + Office.get_query()
            + """
            }
            email
            full_name
            gender
            __typename
        """
        )


class Office(ExpaModel):
    id: int
    name: str
    full_name: str
    parent: Office | None

    def __init__(
        self, id: int, name: str, full_name: str, parent: Office | None
    ):
        super().__init__()
        self.id = id
        self.name = name
        self.full_name = full_name
        self.parent = parent

    def __str__(self) -> str:
        parent = ""
        if self.parent is not None:
            parent = f" ({self.parent})"
        return f"{self.full_name}{parent}"

    @staticmethod
    def from_dict(d: Dict) -> Office:
        parent = None
        if "parent" in d:
            parent = Office.from_dict(d["parent"])

        return Office(d["id"], d["name"], d["full_name"], parent)

    @staticmethod
    def get_query() -> str:
        return """
            id
            name
            full_name
            parent {
              id
              name
              full_name
            }
            __typename
        """
