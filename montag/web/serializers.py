from pydantic import BaseModel


def list_of_models(models: list[BaseModel]) -> list[dict]:
    return [m.dict() for m in models]
