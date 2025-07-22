from app.core.database import Base, engine

def init():
    Base.metadata.create_all(bind=engine)
    print("DB 초기화 완료")

if __name__ == "__main__":
    init()
