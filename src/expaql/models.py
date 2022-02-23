from __future__ import annotations
from typing import Dict, List, Optional
from abc import ABC

from datetime import datetime
from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class ApplicationStatus(str, Enum):
    OPEN = "open"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    APPROVED = "approved"
    WITHDRAWN = "withdrawn"
    REALIZED = "realized"
    FINISHED = "finished"
    COMPLETED = "completed"


class ExpaModel(ABC):
    @staticmethod
    def from_dict(d: Dict) -> ExpaModel | None:
        if d["__typename"] == "CurrentPerson":
            return CurrentPerson.from_dict(d)
        elif d["__typename"] == "Office":
            return Office.from_dict(d)
        else:
            return None


class ContactInfo(ExpaModel):
    country_code: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    facebook: Optional[str]
    instagram: Optional[str]
    linkedin: Optional[str]
    twitter: Optional[str]

    def __init__(
        self,
        country_code: Optional[str],
        phone: Optional[str],
        email: Optional[str],
        facebook: Optional[str],
        instagram: Optional[str],
        linkedin: Optional[str],
        twitter: Optional[str],
    ):
        super().__init__()
        self.country_code = country_code
        self.phone = phone
        self.email = email
        self.facebook = facebook
        self.instagram = instagram
        self.linkedin = linkedin
        self.twitter = twitter

    @staticmethod
    def from_dict(d: Dict) -> ContactInfo:
        return ContactInfo(
            d["country_code"],
            d["phone"],
            d["email"],
            d["facebook"],
            d["instagram"],
            d["linkedin"],
            d["twitter"],
        )

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
            __typename
        """


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
    parent: Optional[Office]

    def __init__(
        self, id: int, name: str, full_name: str, parent: Optional[Office]
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


class City(ExpaModel):
    id: int
    city_details: str
    country: str
    google_place_id: str

    def __init__(
        self, id: int, city_details: str, country: str, google_place_id: str
    ):
        super().__init__()
        self.id = id
        self.city_details = city_details
        self.country = country
        self.google_place_id = google_place_id

    @staticmethod
    def from_dict(d: Dict) -> City:
        return City(
            d["id"], d["city_details"], d["country"], d["google_place_id"]
        )

    @staticmethod
    def get_query() -> str:
        return """
            id
            city_details
            country
            google_place_id
            __typename
        """


class Organisation(ExpaModel):
    id: int
    name: str
    website: str
    contact_detail: ContactInfo

    def __init__(
        self, id: int, name: str, website: str, contact_detail: ContactInfo
    ):
        super().__init__()
        self.id = id
        self.name = name
        self.website = website
        self.contact_detail = contact_detail

    @staticmethod
    def from_dict(d: Dict) -> Organisation:
        return Organisation(
            d["id"],
            d["name"],
            d["website"],
            ContactInfo.from_dict(d["contact_detail"]),
        )

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
            __typename
        """
        )


class Oportunity(ExpaModel):
    id: int
    accepted_count: int
    applicants_count: int
    city: Optional[City]
    description: str
    google_place_id: str
    languages: List[str]
    lat: str
    lng: str
    location: str
    openings: int
    organisation: Organisation
    percentage_of_fulfillment: float
    profile_photo: str
    skills: List[str]
    title: str

    def __init__(
        self,
        id: int,
        accepted_count: int,
        applicants_count: int,
        city: Optional[City],
        description: str,
        google_place_id: str,
        languages: List[str],
        lat: str,
        lng: str,
        location: str,
        openings: int,
        organisation: Organisation,
        percentage_of_fulfillment: float,
        profile_photo: str,
        skills: List[str],
        title: str,
    ):
        super().__init__()
        self.id = id
        self.accepted_count = accepted_count
        self.applicants_count = applicants_count
        self.city = city
        self.description = description
        self.google_place_id = google_place_id
        self.languages = languages
        self.lat = lat
        self.lng = lng
        self.location = location
        self.openings = openings
        self.organisation = organisation
        self.percentage_of_fulfillment = percentage_of_fulfillment
        self.profile_photo = profile_photo
        self.skills = skills
        self.title = title

    def __str__(self) -> str:
        return f"#{self.id} {self.title}"

    @staticmethod
    def from_dict(d: Dict) -> Oportunity:
        if "city" in d and d["city"] is not None:
            city = City.from_dict(d["city"])
        else:
            city = None

        return Oportunity(
            d["id"],
            d["accepted_count"],
            d["applicants_count"],
            city,
            d["description"],
            d["google_place_id"],
            d["languages"],
            d["lat"],
            d["lng"],
            d["location"],
            d["openings"],
            Organisation.from_dict(d["organisation"]),
            d["percentage_of_fulfillment"],
            d["profile_photo"],
            d["skills"],
            d["title"],
        )

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
            languages {
                constant_name
            }
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
            __typename
        """
        )


class OportunityApplication(ExpaModel):
    id: int
    created_at: datetime
    current_status: ApplicationStatus
    experience_end_date: datetime
    experience_start_date: datetime
    opportunity: Oportunity
    person: Person
    questionnaire_answers: str
    standards: List[str]
    status: ApplicationStatus

    def __init__(
        self,
        id: int,
        created_at: datetime,
        current_status: ApplicationStatus,
        experience_end_date: datetime,
        experience_start_date: datetime,
        opportunity: Oportunity,
        person: Person,
        questionnaire_answers: str,
        standards: List[str],
        status: ApplicationStatus,
    ):
        super().__init__()
        self.id = id
        self.created_at = created_at
        self.current_status = current_status
        self.experience_end_date = experience_end_date
        self.experience_start_date = experience_start_date
        self.opportunity = opportunity
        self.person = person
        self.questionnaire_answers = questionnaire_answers
        self.standards = standards
        self.status = status

    def __str__(self) -> str:
        return f"{self.person} from {self.opportunity} ({self.status})"

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def from_dict(d: Dict) -> OportunityApplication:
        return OportunityApplication(
            d["id"],
            d["created_at"],
            ApplicationStatus(d["current_status"]),
            d["experience_end_date"],
            d["experience_start_date"],
            Oportunity.from_dict(d["opportunity"]),
            Person.from_dict(d["person"]),
            d["questionnaire_answers"],
            [it["constant_name"] for it in d["standards"]],
            ApplicationStatus(d["status"]),
        )

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
            + Oportunity.get_query()
            + """
            }
            person {
                """
            + Person.get_query()
            + """
            }
            questionnaire_answers
            standards {
                constant_name
            }
            status
            __typename
        """
        )


class Person(ExpaModel):
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
    nationalities: List[str]
    backgrounds: List[str]
    skills: List[str]
    languages: List[str]

    def __init__(
        self,
        id: int,
        full_name: str,
        contact_detail: Optional[ContactInfo],
        email: str,
        cv_url: str,
        gender: Gender,
        home_lc: str,
        home_mc: str,
        profile_photo: str,
        status: str,
        nationalities: List[str],
        backgrounds: List[str],
        skills: List[str],
        languages: List[str],
    ):
        super().__init__()
        self.id = id
        self.full_name = full_name
        self.contact_detail = contact_detail
        self.email = email
        self.cv_url = cv_url
        self.gender = gender
        self.home_lc = home_lc
        self.home_mc = home_mc
        self.profile_photo = profile_photo
        self.status = status
        self.nationalities = nationalities
        self.backgrounds = backgrounds
        self.skills = skills
        self.languages = languages

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
            }
            __typename
        """
        )

    @staticmethod
    def from_dict(d: Dict) -> Person:
        if "contact_detail" in d:
            contact_detail = ContactInfo.from_dict(d["contact_detail"])
        else:
            contact_detail = None

        nationalities = [
            it["name"] for it in d["person_profile"]["nationalities"]
        ]
        backgrounds = [it["name"] for it in d["person_profile"]["backgrounds"]]
        skills = [it["constant_name"] for it in d["person_profile"]["skills"]]
        languages = [
            it["constant_name"] for it in d["person_profile"]["languages"]
        ]

        return Person(
            d["id"],
            d["full_name"],
            contact_detail,
            d["email"],
            d["cv_url"],
            Gender(d["gender"].lower()),
            d["home_lc"]["name"],
            d["home_mc"]["name"],
            d["profile_photo"],
            d["status"],
            nationalities,
            backgrounds,
            skills,
            languages,
        )
