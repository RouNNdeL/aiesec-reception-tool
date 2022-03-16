from __future__ import annotations

from typing import Any, Dict

import discord
from discord.ext import tasks

from receptiontool.config import IgvToolConfig
from receptiontool.expaql.api import ExpaQuery
from receptiontool.expaql.formaters import OpportunityApplicationFormatter

max_discord_message_length = 1500
person_to_emoji_dict = {
    "Michał": "\N{Grinning Face}",
    "Paweł": "\N{Neutral Face}",
    "Krzysztof": "\N{Thinking Face}",
    "Bartek": "\N{Kissing Face}",
    "Marcin": "\N{money-mouth face}",
    "Maciek": "\N{unamused face}",
}

config = IgvToolConfig()


class MyClient(discord.Client):
    def __init__(self, *args: str, **kwargs: int) -> None:
        super().__init__(*args, **kwargs)
        self.send_new_applications.start()

    async def on_ready(self) -> None:
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")

    @tasks.loop(seconds=300)
    async def send_new_applications(self) -> None:
        channel = self.get_channel(config.discord.dc_channel_id)

        # get applications from db
        expaql = connect_to_expaql()
        applications = expaql.get_applications()

        with open(config.discord.dc_messages_filename, "r") as f:
            dc_messages = f.read().splitlines()

        for application in applications:
            # check if application has already been sent
            if str(application.id) in dc_messages:
                continue

            # send message on discord
            formatter = OpportunityApplicationFormatter(application)
            response = await channel.send(
                f"{formatter.format_markdown()[:max_discord_message_length]}\n\n"
                f"{dictionary_to_string(person_to_emoji_dict)}"
            )

            # add reactions to message
            for person in person_to_emoji_dict:
                await response.add_reaction(person_to_emoji_dict[person])

            # save application id in "discord_messages"
            with open("discord_messages", "a") as f:
                f.write(f"{application.id}\n")

    @send_new_applications.before_loop
    async def before_my_task(self) -> None:
        await self.wait_until_ready()

    async def on_raw_reaction_add(
        self, payload: discord.RawReactionActionEvent
    ) -> None:
        if payload.user_id == self.user.id:
            return
        print(
            f"Application [{payload.message_id}]: assigned to "
            f"{get_key_from_value(person_to_emoji_dict, str(payload.emoji))}."
        )
        # TODO
        # check if card is on trello
        # if it's, add assigment to person

    async def on_raw_reaction_remove(
        self, payload: discord.RawReactionActionEvent
    ) -> None:
        if payload.user_id == self.user.id:
            return
        print(
            f"Application [{payload.message_id}]: removed assignment to "
            f"{get_key_from_value(person_to_emoji_dict, str(payload.emoji))}."
        )
        # TODO


# connect to expaql and save new refresh token
def connect_to_expaql() -> ExpaQuery:
    with open(config.token_file, "r") as f:
        refresh_token = f.read().strip()

    expaql = ExpaQuery(config.expa.client_id, config.expa.client_secret, refresh_token)

    if expaql is not None:
        with open(config.token_file, "w") as f:
            f.write(expaql.get_refresh_token())

    return expaql


def get_key_from_value(dictionary: Dict, value: str | None = None) -> str | Any:
    return [key for key, val in dictionary.items() if val == value][0]


def dictionary_to_string(dictionary: Dict) -> str:
    ret_str = ""
    for key, val in dictionary.items():
        ret_str += f"{val} - {key}\n"
    return ret_str


def bot_start() -> None:
    client = MyClient()
    client.run(config.discord.dc_token)
