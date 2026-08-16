from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openrouter_api_key: str = ""
    deepseek_api_key: str = ""
    minimax_api_key: str = ""
    zai_api_key: str = ""
    moonshot_api_key: str = ""
    mistral_api_key: str = ""
    groq_api_key: str = ""
    deepinfra_api_key: str = ""
    fireworks_api_key: str = ""
    cerebras_api_key: str = ""

    supabase_url: str = "https://bbckbcusqbdgcxnnimus.supabase.co"
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    supabase_secret_key: str = ""
    database_url: str = ""
    jarvis_projects_root: str = "projects"
    worker: str = "openhands"
    task_timeout_sec: int = 1800
    daily_spend_cap_usd: float = 50.0
    model_portfolio: str = "B"
    model_config_dir: str = "config"

    # Deprecated: ignored by Portfolio B agent router (kept for old .env files)
    tier0_model: str = ""
    tier1_model: str = ""
    tier2_model: str = ""
    tier3_model: str = ""


def get_settings() -> Settings:
    return Settings()
