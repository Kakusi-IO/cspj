from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

engine = create_engine(f'mysql+pymysql://{"win"}:{"123-09qwe"}@{"82.157.251.139"}/{"cspj"}')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = automap_base()
Base.prepare(engine, reflect=True)

class DBManager:
    def __init__(self):
        self.session: Session | None = None
    def __enter__(self):
        self.session = SessionLocal()
        return self.session
    def __exit__(self, *args):
        # print('DB_Manager exit.')        
        self.session.close()