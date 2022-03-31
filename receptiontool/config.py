from __future__ import annotations

import os
from typing import Any, Dict, Final, List, Optional

from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable
from pydantic.main import BaseModel
import yaml

ENV_PREFIX: Final = "IGV_"


def yml_config_setting(settings: BaseSettings) -> Dict[str, Any]:
    config_file = os.getenv(f"{ENV_PREFIX}CONFIG")
    if config_file is None:
        config_file = "config.yaml"

    if not os.path.isfile(config_file):
        return {}

    with open(config_file) as f:
        return yaml.safe_load(f)  # type: ignore


class ExpaConfig(BaseModel):
    client_id: str
    client_secret: str
    opportunities: List[int]


class TrelloConfig(BaseModel):
    api_key: str
    token: str
    board_id: str
    list_name: Optional[str] = None


class DiscordConfig(BaseModel):
    webhook_url: str


class IgvToolConfig(BaseSettings):
    expa: ExpaConfig
    trello: TrelloConfig
    discord: DiscordConfig
    token_file: str = ".token"
    data_file: str = ".data"
    log_level: str = "INFO"

    class Config:
        env_prefix = ENV_PREFIX
        env_file = ".env"
        env_nested_delimiter = "__"

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            return (
                init_settings,
                yml_config_setting,
                env_settings,
                file_secret_settings,
            )
