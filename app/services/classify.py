from app.utils.file_parser import parse_csv, parse_json, flatten_rules
from app.crud.transaction import create_transaction_records
from app.crud.company import upsert_company_and_categories

async def process_transactions(bank_csv_file, rules_json_file):
    bank_df = parse_csv(bank_csv_file)
    rules = parse_json(rules_json_file)
    rules = flatten_rules(rules)
    upsert_company_and_categories(rules)

    records, stats = [], {"total": 0, "classified": 0, "unclassified": 0}
    for _, row in bank_df.iterrows():
        tx = row.to_dict()
        match = None
        for company_id, rule_list in rules.items():
            for rule in rule_list:
                if rule["keyword"] in tx["적요"]:
                    match = (company_id, rule["category_id"], rule["category_name"])
                    break
            if match: break

        income = float(tx.get("입금액", 0) or 0)
        outcome = float(tx.get("출금액", 0) or 0)
        amount = income - outcome
        tx.update({
            "company_id": match[0] if match else None,
            "category_id": match[1] if match else None,
            "category_name": match[2] if match else "미분류",
            "classified": bool(match),
            "금액": amount,
        })
        records.append(tx)
        stats["total"] += 1
        stats["classified"] += int(bool(match))
    create_transaction_records(records)
    stats["unclassified"] = stats["total"] - stats["classified"]
    return {"msg": "Processed", **stats}
