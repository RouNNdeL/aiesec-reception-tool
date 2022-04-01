from typing import Any, Dict, Optional

from .models import OpportunityApplication


class OpAppFormatter:
    @staticmethod
    def format_markdown(app: OpportunityApplication) -> str:
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

    @staticmethod
    def format_discord_embed(
        app: OpportunityApplication,
        url: Optional[str] = None,
        title: Optional[str] = None,
    ) -> Dict[str, Any]:
        _title = "A new application has just been submitted"
        if title is not None:
            _title = title

        fields = []
        if app.person.contact_detail is not None:
            phone_number = app.person.contact_detail.format_phone_number()
            whatsapp_url = app.person.contact_detail.whatsapp_url()

            if phone_number is not None:
                phone_md = f"[{phone_number}]({whatsapp_url})"
                fields.append({"name": "Phone number", "value": phone_md})

        if len(app.person.profile.nationalities) > 0:
            nationalities = ", ".join(app.person.profile.nationalities)
            fields.append({"name": "Nationalities", "value": nationalities})

        if len(app.person.profile.languages) > 0:
            languages = ", ".join(app.person.profile.languages)
            fields.append({"name": "Languages", "value": languages})

        cv = app.get_cv(safe=True)
        if cv is not None:
            cv_md = f"[Click here]({cv})"
            fields.append({"name": "Resume", "value": cv_md})

        author = {"name": app.person.full_name, "url": app.expa_url()}

        if app.person.profile_photo.endswith(("png", "jpg")):
            author["icon_url"] = app.person.profile_photo

        embed = {
            "title": _title,
            "description": f"New application for [*{app.opportunity.title}*]({app.opportunity.expa_url()})",
            "timestamp": app.created_at.isoformat(),
            "url": url,
            "author": author,
            "fields": fields,
            "footer": {"text": "Application date"},
        }

        return embed
