from .models import OportunityApplication


class OportunityApplicationFormatter:
    __oportunity_application: OportunityApplication

    def __init__(self, oportunity_application: OportunityApplication):
        self.__oportunity_application = oportunity_application

    def format_markdown(self) -> str:
        app = self.__oportunity_application
        person = app.person

        languages = ""
        if len(person.languages) > 0:
            languages = "### Languages\n"
            for language in person.languages:
                languages += f" - {language}\n"

        nationalities = ""
        if len(person.nationalities) > 0:
            nationalities = "### Nationalities\n"
            for nationality in person.nationalities:
                nationalities += f" - {nationality}\n"

        backgrounds = ""
        if len(person.backgrounds) > 0:
            backgrounds = "### Backgrounds\n"
            for background in person.backgrounds:
                backgrounds += f" - {background}\n"

        skills = ""
        if len(person.skills) > 0:
            skills = "### Skills\n"
            for skill in person.skills:
                skills += f" - {skill}\n"

        about = ""
        if app.gip_answer is not None:
            about = app.gip_answer

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
                    f"Instagram: [{handle}]"
                    f"(https://www.instagram.com/{handle})"
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
        """
