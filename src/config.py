from pydantic import BaseSettings


class IgvToolConfig(BaseSettings):
    expa_client_id: str
    expa_client_secret: str
    token_file: str = ".token"
    log_level: str = "INFO"
    trello_api_key: str
    trello_token: str
    trello_board_id: str

    class Config:
        env_prefix = "igv_"
        env_file = ".env"
