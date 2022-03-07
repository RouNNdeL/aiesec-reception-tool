import os
from pydantic.main import BaseModel
import yaml

from typing import Any, Dict, Final
from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable

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


class IgvToolConfig(BaseSettings):
    expa: ExpaConfig
    token_file: str = ".token"
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
