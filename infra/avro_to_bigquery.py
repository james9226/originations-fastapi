import json
import sys
import ast

avro_to_bigquery_type_map = {
    "string": "STRING",
    "int": "INTEGER",
    "long": "INT64",
    "float": "FLOAT",
    "double": "FLOAT64",
    "boolean": "BOOL",
    "bytes": "BYTES",
    "null": "STRING",  # BigQuery doesn't have a direct equivalent to Avro's null type
}


def type_lookup(avro_name: str, avro_type: str):
    time_fields = ["time", "date"]

    if any(x in avro_name.lower() for x in time_fields):
        return "TIMESTAMP"

    return avro_to_bigquery_type_map[avro_type]


def avro_field_to_bigquery_field(avro_field):
    return {
        "name": avro_field["name"],
        "type": type_lookup(avro_field["name"], avro_field["type"]),
    }


def avro_schema_to_bigquery_schema(avro_schema: dict):
    # raise ValueError(avro_schema)
    avro_fields = avro_schema.get("fields")
    return [avro_field_to_bigquery_field(field) for field in avro_fields]


if __name__ == "__main__":
    input = sys.stdin.read()
    avro_schema_path = ast.literal_eval(input)["avro_schema"]
    with open(avro_schema_path) as r:
        avro_schema = json.load(r)

    bigquery_schema = avro_schema_to_bigquery_schema(avro_schema)
    result = {"converted_schema": json.dumps(bigquery_schema)}
    json.dump(result, sys.stdout)
