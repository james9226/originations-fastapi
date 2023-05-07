import json


def load_schema(schema_name: str) -> dict:
    SCHEMA_BASE_PATH = "originations/schemas/"

    with open(SCHEMA_BASE_PATH + schema_name + ".json") as raw_json:
        x = json.load(raw_json)

    return x
