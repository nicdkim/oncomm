import pandas as pd
import json

def parse_csv(file):
    file.file.seek(0)
    return pd.read_csv(file.file)

def parse_json(file):
    file.file.seek(0)
    return json.load(file.file)
