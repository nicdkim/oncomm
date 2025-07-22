from app.models.company import Company
from app.models.category import Category
from app.core.database import SessionLocal

def upsert_company_and_categories(rules: dict):
    session = SessionLocal()
    try:
        for company_id, rule_list in rules.items():
            if not session.query(Company).filter_by(id=company_id).first():
                session.add(Company(id=company_id, name=company_id))
            for rule in rule_list:
                cat_id = rule["category_id"]
                cat_name = rule["category_name"]
                if not session.query(Category).filter_by(id=cat_id).first():
                    session.add(Category(id=cat_id, name=cat_name, company_id=company_id))
        session.commit()
    finally:
        session.close()
