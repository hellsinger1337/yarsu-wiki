from app.db.database import Base, engine
from sqlalchemy.orm import Session
from app.models.user import User

def init_db():
    Base.metadata.create_all(bind=engine)

def clear_users_table(db: Session):
    db.query(User).delete()
    db.commit()