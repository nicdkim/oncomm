import pandas as pd
import json

def parse_csv(file):
    file.file.seek(0)
    return pd.read_csv(file.file)

def parse_json(file):
    file.file.seek(0)
    return json.load(file.file)

def flatten_rules(json_rules):
    output = {}
    for company in json_rules["companies"]:
        company_id = company["company_id"]
        arr = []
        for category in company["categories"]:
            cat_id = category["category_id"]
            cat_name = category["category_name"]
            for kw in category["keywords"]:
                arr.append({
                    "keyword": kw,
                    "category_id": cat_id,
                    "category_name": cat_name
                })
        output[company_id] = arr
    return output
