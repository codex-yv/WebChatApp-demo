from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from starlette.status import HTTP_303_SEE_OTHER
from schemas.loginSchemas import Loign
from schemas.signupSchemas import SignUp
from utils.userDBposts import create_user
from utils.usersDBgets import get_all_user, get_user_cred
from utils.userPuts import update_user_status
from utils.chatsDB import create_chat_history_db
from utils.chatsDBposts import insert_chat
from utils.chatsDBgets import get_all_chats
import json


class Password:
    def __init__(self, password):
        self.password = password

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="qwertyuiopasdfghjkl@#$%RTYU")
# Jinja2 template directory
templates = Jinja2Templates(directory="templates")

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store connected users
connected_users = {}


@app.get("/")
async def get(request: Request):

    await create_chat_history_db()
    return {"Message":"Welcome"}

@app.get("/login", response_class=HTMLResponse)
async def Login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register",response_class=HTMLResponse)
async def Register(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(user_id: str, websocket: WebSocket):
    await websocket.accept()

    connected_users[user_id] = websocket
    print(f"Connected users: {connected_users.keys()}")
    
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from {user_id}: {data}")
            await insert_chat(user_id, data)
            # Broadcast to other users
            for user, user_ws in connected_users.items():
                if user != user_id:
                    await user_ws.send_text(f"{user_id}: {data}")

            
    except WebSocketDisconnect:
        print(f"{user_id} disconnected")
        # await insert_chat(user_id, "disconnected")

        for user, user_ws in connected_users.items():
            if user != user_id:
                await user_ws.send_text(f"{user_id}: disconnected")
        try:
            del connected_users[user_id]
        except KeyError:
            pass

    finally:
        # Do not try to close if already closed
        if not websocket.client_state.name == "DISCONNECTED":
            try:
                await websocket.close()
            except RuntimeError:
                pass  # Silently ignore double close attempts

@app.post("/login")
async def submitLogin(request: Request, values:Loign = Form(...)):
    data = await get_all_user()
    if values.username in data:
        password_get = await get_user_cred(collection_name=values.username)
        password = password_get[0]["password"]

        request.session["username"] = values.username
        request.session["password"] = password


        await update_user_status(collection_name=values.username, password_value= values.password, new_status="ACTIVE")
        if values.password == password:
            chat_data = get_all_chats()
            contacts = ["Liam", "Sophia", "Ethan"]
            return templates.TemplateResponse("index.html", {"request": request, "user": values.username, "chat_history":chat_data, "contacts": contacts})
        else:
            return {"Message":"Invalid Password"}
    else:
        return {"Message":"Invalid Username"}
    
@app.post("/register")
async def submitRegister(request: Request, values:SignUp = Form(...)):
    data = await get_all_user()
    if values.username not in data:
        new_data = {
            "password":values.password,
            "status":"ACTIVE",
            "contacts":[],
            "key":""
        }
        await create_user(collection_name=values.username, user_data=new_data)

        request.session["username"] = values.username
        request.session["password"] = values.password

        chat_data = get_all_chats()
        contacts = ["Liam", "Sophia", "Ethan"]
        return templates.TemplateResponse("index.html", {"request": request, "user": values.username, "chat_history":chat_data, "contacts": contacts})
    else:
        return {"Message":"User already exist!"}
    

from fastapi import Body

@app.post("/chat-history")
async def chat_history(data: dict = Body(...)):
    user = data.get("user")
    contact = data.get("contact")
    print(user)
    print(contact)
    # Dummy data → Replace with DB logic
    sample_history = {
        ("yv856", "Sophia"): [("yv856", "Hey Sophia!"), ("Sophia", "Hi Liam!")],
        ("admin", "Ethan"): [("admin", "Hello Ethan"), ("Ethan", "Hey Sophia!")],
    }
    
    # Get both directions of conversation
    history = sample_history.get((user, contact), []) + sample_history.get((contact, user), [])
    print(history)
    return history
