from app.core.database import Base, engine
from app.models import company, category, transaction

import sqlalchemy

def init():
    Base.metadata.create_all(bind=engine)
    print("DB 초기화 완료")
    insp = sqlalchemy.inspect(engine)
    print("DB 테이블:", insp.get_table_names())

if __name__ == "__main__":
    init()
