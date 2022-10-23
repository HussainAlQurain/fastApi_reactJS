from ast import For
from fastapi import FastAPI, Path, Query, Request, Form
from enum import Enum
from pydantic import BaseModel, HttpUrl
import requests, bs4, re
from my_modules.thumbnail import find_img
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from steam.client import SteamClient
from dota2.client import Dota2Client

client = SteamClient()
dota = Dota2Client(client)

@client.on('logged_on')
def start_dota():
    dota.launch()


app = FastAPI()

templates = Jinja2Templates(directory="static")


# todos = [
#     {
#         "id": "1",
#         "item": "Read a book."
#     },
#     {
#         "id": "2",
#         "item": "Cycle around town."
#     }
# ]



# origins = [
#     "http://localhost:3000",
#     "localhost:3000"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )


@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse('home.html', {"request": request, "user":'Hussain'})

@app.post('/')
async def get_thumbnail(request: Request, url: str = Form(...)):
    tmp = find_img(url)
    return templates.TemplateResponse('results.html', {"request":request, "result": tmp})


#@app.get('/dota/')
#async def dota_page():
#    return templates.TemplateResponse('player_details.html')

@app.get('/search_player')
async def search_player(request: Request):
    return templates.TemplateResponse('search_player.html', context={'request': request, 'results': "result"})


@app.post('/search_player')
async def get_player(request: Request, player_id: int = Form(...)):
    client.cli_login(username="",password="")
    jobid = dota.request_profile(player_id)
    profile_card = dota.wait_msg(jobid, timeout=10)
    

    count = 1
    while profile_card is None:
        jobid = dota.request_profile(player_id)
        count +=1
        profile_card = dota.wait_msg(jobid, timeout=10)
        if count > 10:
            break
    dota.exit()
    client.logout()

    dota.exit()
    client.logout()
    return templates.TemplateResponse('search_player.html', context={'request': request, 'results': profile_card})

# @app.get("/todo", tags=["todos"])
# async def get_todos() -> dict:
#     return { "data": todos }


# @app.post("/todo", tags=["todos"])
# async def add_todo(todo: dict) -> dict:
#     todos.append(todo)
#     return {
#         "data": { "Todo added." }
#     }


# @app.put("/todo/{id}", tags=["todos"])
# async def update_todo(id: int, body: dict) -> dict:
#     for todo in todos:
#         if int(todo["id"]) == id:
#             todo["item"] = body["item"]
#             return {
#                 "data": f"Todo with id {id} has been updated."
#             }

#     return {
#         "data": f"Todo with id {id} not found."
#     }

# @app.delete("/todo/{id}", tags=["todos"])
# async def delete_todo(id: int) -> dict:
#     for todo in todos:
#         if int(todo["id"]) == id:
#             todos.remove(todo)
#             return {
#                 "data": f"Todo with id {id} has been removed."
#             }

#     return {
#         "data": f"Todo with id {id} not found."
#     }

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=80, reload=True)
