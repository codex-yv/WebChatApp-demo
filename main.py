from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Form, Body
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from starlette.status import HTTP_303_SEE_OTHER
from schemas.loginSchemas import Loign
from schemas.signupSchemas import SignUp
from utils.userDBposts import create_user
from utils.usersDBgets import get_all_user, get_user_cred, get_all_keys, get_user_cred_key, get_user_cred_contacts, get_user_contacts_key, get_user_status
from utils.userPuts import update_user_cred_one, update_user_contact, update_contact_keys,update_last_seen
from utils.chatsDB import create_contact
from utils.chatsDBposts import insert_chat
from utils.chatsDBgets import get_chat
from utils.IST import ISTtime
from security.encryptChat import encryptt
import json

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="qwertyuiopasdfghjkl@#$%RTYU")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_users = {}

@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(user_id: str, websocket: WebSocket):
    await websocket.accept()
    connected_users[user_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            
            try:
                payload = json.loads(data)
                recipient = payload.get("to")
                message = payload.get("msg")
                
                if not recipient or not message:
                    continue
                    
                # Save chat
                contact_key = await get_user_contacts_key(collection_name=user_id, contact_name=recipient)
                await insert_chat(collection_name=contact_key, user=user_id, message=message)
                
                # Send to recipient only if they're connected
                if recipient in connected_users:
                    try:
                        await connected_users[recipient].send_text(f"{user_id}: {message}")
                    except Exception:
                        # If sending fails, the recipient might have disconnected
                        pass
                        
            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(f"Error processing message: {e}")
                continue

    except WebSocketDisconnect:
        # FIXED: No longer trying to send messages on disconnect
        pass
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        # Clean up connection
        if user_id in connected_users:
            await update_last_seen(collection_name=user_id)
            del connected_users[user_id]
        try:
            await websocket.close()
        except Exception:
            pass

@app.post("/login")
async def submitLogin(request: Request, values: Loign = Form(...)):
    data = await get_all_user()
    if values.username in data:
        password_get = await get_user_cred(collection_name=values.username)
        password = password_get[0]["password"]

        request.session["username"] = values.username
        request.session["password"] = password

        await update_user_cred_one(collection_name=values.username, password_value=values.password, field_name="status", new_value="ACTIVE")
        
        if values.password == password:
            contacts = await get_user_cred_contacts(collection_name=values.username)
            return templates.TemplateResponse("index.html", {"request": request, "user": values.username, "chat_history": [], "contacts": contacts})
        else:
            return 102
    else:
        return 101

@app.post("/register")
async def submitRegister(request: Request, values: SignUp = Form(...)):
    data = await get_all_user()
    if values.username not in data:
        new_data = {
            "password": values.password,
            "status": "ACTIVE",
            "contacts": [],
            "contact_keys": {},
            "key": ""
        }
        await create_user(collection_name=values.username, user_data=new_data)

        request.session["username"] = values.username
        request.session["password"] = values.password

        contacts = await get_user_cred_contacts(collection_name=values.username)
        
        return templates.TemplateResponse("index.html", {"request": request, "user": values.username, "chat_history": [], "contacts": contacts})
    else:
        return 0

@app.post("/chat-history")
async def chat_history(data: dict = Body(...)):
    user = data.get("user")
    contact = data.get("contact")
    
    contact_key = await get_user_contacts_key(collection_name=user, contact_name=contact)
    chat_data = await get_chat(collection_name=contact_key)
    
    sample_history = {
        (user, contact): chat_data,
    }
    if contact in connected_users:
        status = "Online"
    else:
        status = await get_user_status(contact)

    history = sample_history.get((user, contact), []) + sample_history.get((contact, user), [])
    return history, status

@app.post("/save-unique-id")
async def update_id(request: Request, data: dict = Body(...)):
    unique_id = data.get("unique_id")
    all_keys = await get_all_keys()

    if unique_id not in all_keys:
        await update_user_cred_one(collection_name=request.session.get("username"),
                                 password_value=request.session.get("password"), field_name="key", new_value=unique_id)
        return JSONResponse({"success": True})
    else:
        return JSONResponse({"success": False})

@app.post("/connect-user")
async def connect_user(request: Request, data: dict = Body(...)):
    new_user = data.get("username")
    key = data.get("key")
    current_user = request.session.get("username")
    all_users = await get_all_user()
    
    if new_user in all_users and new_user != current_user:
        get_key = await get_user_cred_key(collection_name=new_user)
        if get_key == key:
            await update_user_contact(collection_name=new_user, field_name="key", field_value=get_key, new_contact=current_user)
            await update_user_contact(collection_name=current_user, field_name="password", field_value=request.session.get("password"), new_contact=new_user)
            
            contact_format = new_user + current_user 
            await update_contact_keys(collection_name=current_user, field_name="password", field_value=request.session.get("password"), new_contact=new_user, key=contact_format)
            await update_contact_keys(collection_name=new_user, field_name="key", field_value=key, new_contact=current_user, key=contact_format)

            keyy, token = encryptt(chat="INITIATED THE CHAT")
            current_time = ISTtime()
            chat = {
                "user": current_user,
                "message": token,
                "key": keyy,
                "time": current_time
            }
            
            await create_contact(collection_name=contact_format, user_data=chat)
            contact_list = await get_user_cred_contacts(collection_name=current_user)    
            return contact_list
    return False