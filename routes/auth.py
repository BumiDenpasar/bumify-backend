from fastapi import HTTPException, APIRouter, Depends
import bcrypt, uuid
from models.user import User
from pydantic_schemas.signup import UserCreate
from database import get_db
from sqlalchemy.orm import Session

r = APIRouter()

@r.post("/signup")
def signup(u: UserCreate, db: Session=Depends(get_db)):
    name = u.name
    email = u.email
    password = bcrypt.hashpw(u.password.encode(), bcrypt.gensalt())

    print(name, email)

    user_db = db.query(User).filter(User.email == email).first()
    if user_db:
        raise HTTPException(400, "Email already exists")

    user_db = User(id=str(uuid.uuid4()), name=name, email=email, password=password)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)  
    print('success')

    return user_db
