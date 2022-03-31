from __future__ import annotations

from datetime import datetime
from enum import Enum
import re
from typing import Any, Dict, List, Optional, Set

from pydantic import BaseModel, Extra, Field, validator


def flatten_name(d: Dict[str, str]) -> str:
    if "constant_name" in d:
        return d["constant_name"]

    if "name" in d:
        return d["name"]

    raise KeyError("Neither 'constant_name' nor 'name' key found in dict")


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

    def get_pronoun(self) -> str:
        if self == Gender.MALE:
            return "he"
        if self == Gender.FEMALE:
            return "she"

        return "they"


class ApplicationStatus(str, Enum):
    OPEN = "open"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    APPROVED = "approved"
    WITHDRAWN = "withdrawn"
    REALIZED = "realized"
    FINISHED = "finished"
    COMPLETED = "completed"
    APPROVAL_BROKEN = "approval_broken"


class ContactInfo(BaseModel, extra=Extra.forbid):
    country_code: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    facebook: Optional[str]
    instagram: Optional[str]
    linkedin: Optional[str]
    twitter: Optional[str]

    @validator("phone", pre=True)
    def normalize_phone(cls: Any, v: Any) -> Optional[str]:
        if isinstance(v, str):
            return re.sub(re.compile(r"[^\d]"), "", v)

        return None

    def format_phone_number(self) -> str:
        return f"{self.country_code} {self.phone}"

    def whatsapp_url(self) -> str:
        return f"https://wa.me/{self.country_code}{self.phone}"

    @staticmethod
    def get_query() -> str:
        return """
            country_code
            phone
            email
            facebook
            instagram
            linkedin
            twitter
        """


class GqlSchemaField(BaseModel, extra=Extra.forbid):
    name: str
    type: str

    @validator("type", pre=True)
    def get_type(cls: Any, v: Any) -> str:
        assert isinstance(v, dict)

        if v["name"] is not None:
            assert isinstance(v["name"], str)

            return v["name"]

        assert isinstance(v["kind"], str)

        return v["kind"]


class GqlSchema(BaseModel, extra=Extra.forbid):
    name: str
    fields: List[GqlSchemaField]


class CurrentPerson(BaseModel, extra=Extra.forbid):
    id: int
    aiesec_email: str
    cover_photo: str
    created_at: datetime
    current_office: Office
    email: str
    full_name: str
    gender: Gender

    def __str__(self) -> str:
        return f"{self.full_name} from {self.current_office}"

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
        """
        )


class Office(BaseModel, extra=Extra.forbid):
    id: int
    name: str
    full_name: str
    parent: Optional[Office]

    def __str__(self) -> str:
        parent = ""
        if self.parent is not None:
            parent = f" ({self.parent})"
        return f"{self.full_name}{parent}"

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
        """


class City(BaseModel, extra=Extra.forbid):
    id: int
    city_details: str
    country: str
    google_place_id: str

    @staticmethod
    def get_query() -> str:
        return """
            id
            city_details
            country
            google_place_id
        """


class Organisation(BaseModel, extra=Extra.forbid):
    id: int
    name: str
    website: Optional[str]
    contact_detail: ContactInfo

    @staticmethod
    def get_query() -> str:
        return (
            """
            id
            name
            website
            contact_detail {
                """
            + ContactInfo.get_query()
            + """
            }
        """
        )


class Opportunity(BaseModel, extra=Extra.forbid):
    id: int
    accepted_count: int
    applicants_count: int
    city: Optional[City]
    description: str
    google_place_id: str
    lat: str
    lng: str
    location: str
    openings: int
    organisation: Organisation
    percentage_of_fulfillment: float
    profile_photo: str
    skills: List[str]
    title: str

    @validator("skills", pre=True, each_item=True)
    def flatten_constant(cls: Opportunity, v: Any) -> str:
        return flatten_name(v)

    def expa_url(self) -> str:
        return f"https://expa.aiesec.org/opportunities/{self.id}"

    @staticmethod
    def get_query() -> str:
        return (
            """
            id
            accepted_count
            applicants_count
            city {
                """
            + City.get_query()
            + """
            }
            description
            google_place_id
            lat
            lng
            location
            openings
            organisation {
                """
            + Organisation.get_query()
            + """
            }
            percentage_of_fulfillment
            profile_photo
            skills {
                constant_name
            }
            title
        """
        )


class PersonProfile(BaseModel, extra=Extra.forbid):
    nationalities: Set[str]
    backgrounds: Set[str]
    skills: Set[str]
    languages: Set[str]

    @validator("nationalities", "backgrounds", "skills", "languages", pre=True)
    def extract_profile(cls: Any, v: Any) -> Set[str]:
        return {flatten_name(it) for it in v}

    @staticmethod
    def get_query() -> str:
        return """
            nationalities {
                name
            }
            backgrounds {
                name
            }
            skills {
                constant_name
            }
            languages {
                constant_name
            }
        """


class Person(BaseModel, extra=Extra.forbid):
    id: int
    full_name: str
    contact_detail: Optional[ContactInfo]
    email: str
    cv_url: str
    gender: Gender
    home_lc: str
    home_mc: str
    profile_photo: str
    status: str
    profile: PersonProfile = Field(alias="person_profile")

    @validator("home_mc", "home_lc", pre=True)
    def office_name(cls: Any, v: Any) -> Optional[str]:
        assert isinstance(v, dict)
        assert "name" in v
        assert isinstance(v["name"], str)

        return v["name"]

    @validator("gender", pre=True)
    def fix_gender_case(cls: Any, v: Any) -> Optional[str]:
        assert isinstance(v, str)

        return v.lower()

    def __str__(self) -> str:
        return f"{self.full_name}"

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def get_query() -> str:
        return (
            """
            id
            full_name
            contact_detail {
                """
            + ContactInfo.get_query()
            + """
            }
            email
            cv_url
            gender
            home_lc {
                name
            }
            home_mc {
                name
            }
            profile_photo
            status
            person_profile {
            """
            + PersonProfile.get_query()
            + """
            }
        """
        )


class ApplicationMetaType(BaseModel, extra=Extra.forbid):
    gip_answer: Optional[str]

    @staticmethod
    def get_query() -> str:
        return """
            answers
            gip_answer
            vd_blog_url
        """


class OpportunityApplication(BaseModel, extra=Extra.forbid):
    id: int
    created_at: datetime
    current_status: ApplicationStatus
    experience_end_date: Optional[datetime]
    experience_start_date: Optional[datetime]
    opportunity: Opportunity
    person: Person
    cv: Optional[str]
    standards: List[str]
    status: ApplicationStatus
    meta: ApplicationMetaType

    @validator("cv", pre=True)
    def extract_cv_url(cls: Any, v: Any) -> Optional[str]:
        if v is None:
            return None

        assert isinstance(v, dict)
        assert "url" in v
        assert isinstance(v["url"], str)

        return v["url"]

    @validator("standards", pre=True, each_item=True)
    def flatten_constant(cls: OpportunityApplication, v: Any) -> str:
        return flatten_name(v)

    def get_cv(self) -> Optional[str]:
        if self.cv is not None:
            return self.cv
        return self.person.cv_url

    def expa_url(self) -> str:
        return f"https://expa.aiesec.org/applications/{self.id}"

    @staticmethod
    def get_query() -> str:
        return (
            """
            id
            created_at
            current_status
            experience_end_date
            experience_start_date
            opportunity {
                """
            + Opportunity.get_query()
            + """
            }
            person {
                """
            + Person.get_query()
            + """
            }
            cv {
                url
            }
            meta {
                gip_answer
            }
            standards {
                constant_name
            }
            status
        """
        )
