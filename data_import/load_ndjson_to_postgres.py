import json
import os

import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine

db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'mimiciv_fhir')
db_user = os.getenv('DB_USER', 'ran')
db_password = os.getenv('DB_PASSWORD', 'M@mba12345678')

# URL-encode the password
encoded_password = quote_plus(db_password)

# Construct the connection string
connection_string = f"postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"

# Create the engine
engine = create_engine(connection_string)

# engine = create_engine(
#     "postgresql://ran:'M@mba12345678'@localhost:5432/mimiciv_fhir"
# )

data_dir = "./physionet.org/files/mimic-iv-fhir-demo/2.0/mimic-fhir"
             


def flatten_data(data):
    """Flatten nested dictionaries/lists in the data."""
    for record in data:
        for key, value in record.items():
            if isinstance(value, list) or isinstance(value, dict):
                record[key] = json.dumps(value)
    return data


def load_ndjson_to_db(file_path, table_name):
    with open(file_path, "r") as f:
        data = [json.loads(line) for line in f]
        data = flatten_data(data)
    df = pd.json_normalize(data)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Loaded {file_path} into {table_name}")


files_to_tables = {
    "Condition.ndjson": "condition",
    "Encounter.ndjson": "encounter",
    "Medication.ndjson": "medication",
    "MedicationAdministration.ndjson": "medication_administration",
    # "MedicationRequest.ndjson": "medication_request",
    # "ObservationChartevents.ndjson": "observation_chartevents",
    # "ObservationLabevents.ndjson": "observation_labevents",
    "Patient.ndjson": "patient",
    "Procedure.ndjson": "procedure",
}

for file_name, table_name in files_to_tables.items():
    file_path = os.path.join(data_dir, file_name)
    if os.path.exists(file_path):
        load_ndjson_to_db(file_path, table_name)
    else:
        print(f"File {file_name} not found in {data_dir}")
