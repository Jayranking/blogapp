# imports
from typing_extensions import deprecated
from uu import encode
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates  
from fastapi.responses import HTMLResponse

from routes.blog import router

# Initialize
app = FastAPI()

# Static file serv
app.mount("/static", StaticFiles(directory="static"), name="static")
# Jinja2 Template directory
templates = Jinja2Templates(directory="templates")



SECRET_KEY = "3njfnjrurr9r9knfjgijigigjigjig8u8y7yh3bjbjhu3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


db = {
    "Godfrey": {
        "firstname": "Godfrey",
        "lastname": "Ani",
        "username": "Jayranking",
        "email": "jayranking81@gmail.com",
        "hashed_password": "$2b$12$kpMkGEXjuWloBtOIwLipdudrsGoBAY2OJjoYUJuZZ2WjwWw9NnKJK",
        "disabled": False
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str 

class User(BaseModel):
    firstname:str 
    lastname: str 
    username: str 
    email: str 
    disabled: bool 

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)
    
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta or None):
    to_encode = data.copy
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HPPT_401_UNAUTHORIZED, 
                                         detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inative user")
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/user", response_model=User)
async def get_users(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/blogs")
async def get_own_blogs(current_user: User = Depends(get_current_active_user)):
    return [{"blog_id": 1, "owner": current_user}]

# pwd = get_password_hash("Godfrey123")
# print(pwd)

# from route folder 
app.include_router(router)


# My Interface 
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/create_blog", response_class=HTMLResponse)
async def create_blog(request: Request):
    return templates.TemplateResponse("create_blog.html", {"request": request})
    
@app.get("/view_blog", response_class=HTMLResponse)
async def view_blog(request: Request):
    return templates.TemplateResponse("view_blog.html", {"request": request})

@app.get("/edit_blog", response_class=HTMLResponse)
async def edit_blog(request: Request):
    return templates.TemplateResponse("edit_blog.html", {"request": request})