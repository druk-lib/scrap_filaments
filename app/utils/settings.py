from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool
    path_debug_data: str
    result_file_path: str

    model_config = SettingsConfigDict(env_file=('config.env', 'debug.env'), env_file_encoding='utf-8')


settings = Settings()
