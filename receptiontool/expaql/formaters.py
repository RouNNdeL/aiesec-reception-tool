from .models import OpportunityApplication


class OpportunityApplicationFormatter:
    __opportunity_application: OpportunityApplication

    def __init__(self, oportunity_application: OpportunityApplication):
        self.__opportunity_application = oportunity_application

    def format_markdown(self) -> str:
        app = self.__opportunity_application
        person = app.person
        opportunity = app.opportunity

        languages = ""
        if len(person.profile.languages) > 0:
            languages = "### Languages\n"
            for language in person.profile.languages:
                languages += f" - {language}\n"

        nationalities = ""
        if len(person.profile.nationalities) > 0:
            nationalities = "### Nationalities\n"
            for nationality in person.profile.nationalities:
                nationalities += f" - {nationality}\n"

        backgrounds = ""
        if len(person.profile.backgrounds) > 0:
            backgrounds = "### Backgrounds\n"
            for background in person.profile.backgrounds:
                backgrounds += f" - {background}\n"

        skills = ""
        if len(person.profile.skills) > 0:
            skills = "### Skills\n"
            for skill in person.profile.skills:
                skills += f" - {skill}\n"

        about = ""
        if app.meta.gip_answer is not None:
            about = app.meta.gip_answer

        c_phone = ""
        c_instagram = ""
        c_email = ""

        if person.contact_detail is not None:
            if person.contact_detail.phone is not None:
                formated_nr = person.contact_detail.format_phone_number()
                whatsapp_url = person.contact_detail.whatsapp_url()
                c_phone = f"Phone number: [{formated_nr}]({whatsapp_url})"

            if person.contact_detail.instagram is not None:
                handle = person.contact_detail.instagram
                c_instagram = (
                    f"Instagram: [{handle}](https://www.instagram.com/{handle})"
                )

            if person.email is not None:
                email = person.email
                c_email = f"Email: [{email}](mailto:{email})"

        return f"""
# {person.full_name}

## Contact info

{c_phone}
{c_instagram}
{c_email}

## About

{about}

{nationalities}

## Application detail
### CV

[Click here]({app.get_cv()})

{languages}
{backgrounds}
{skills}

## Expa
[Application]({app.expa_url()})
[Oportunity]({opportunity.expa_url()})
        """
