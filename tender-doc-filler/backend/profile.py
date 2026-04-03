import json
from pathlib import Path
from .models import CompanyProfile

PROFILE_PATH = Path(__file__).parent / "default_profile.json"


def load_profile() -> CompanyProfile:
    data = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    return CompanyProfile(**data)


def save_profile(profile: CompanyProfile) -> None:
    PROFILE_PATH.write_text(
        json.dumps(profile.model_dump(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
