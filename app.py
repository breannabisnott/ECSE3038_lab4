from typing import Annotated, List, Optional
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, BeforeValidator, TypeAdapter, Field
import uuid
import motor.motor_asyncio
from dotenv import dotenv_values
from bson import ObjectId
from pymongo import ReturnDocument, MongoClient

config = dotenv_values(".env")

client = motor.motor_asyncio.AsyncIOMotorClient(config["MONGO_URL"])
db = client.tank_data

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [ "https://ecse3038-lab3-tester.netlify.app" ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PyObjectId = Annotated[str, BeforeValidator(str)]

class Tank(BaseModel):
    id: Optional[PyObjectId] = Field(alias = "_id", default = None)
    location: Optional[str] = None
    lat: Optional[float] = None
    long: Optional[float] = None

class Profile(BaseModel):
    last_updated: Optional[str] = None
    username: Optional[str] = None
    role: Optional[str] = None
    color: Optional[str] = None

@app.get("/profile")
async def get_profile():
    profile = await db["profiles4"].find().to_list(1)
    return TypeAdapter(List[Profile]).validate_python(profile)

@app.post("/profile", status_code=201)
async def create_profile(profile: Profile):
        
    #insert some if here
        new_profile = await db["profiles4"].insert_one(profile.model_dump())

        created_profile = await db["profiles4"].find_one({"_id": new_profile.inserted_id})
        return Profile(**created_profile)
    #raise HTTPException(status_code = 400, detail = "Unable to create more than 1 profile")


@app.get("/tank")
async def get_tanks():
    tanks = await db["tanks4"].find().to_list(999)
    return TypeAdapter(List[Tank]).validate_python(tanks)

@app.get("/tank/{id}")
async def get_tank(id: str):
    #insert if
        tank = await db["tanks4"].find_one({"_id": ObjectId(id)})
        return Tank(**tank)
    #raise HTTPException(status_code = 404, detail = "Tank of id: " + id + " not found.")

@app.post("/tank", status_code=201)
async def create_tank(tank: Tank):
    new_tank = await db["tanks4"].insert_one(tank.model_dump())

    created_tank = await db["tanks4"].find_one({"_id": new_tank.inserted_id})
    return Tank(**created_tank)

@app.patch("/tank/{id}")
async def update_tank(id: str, tank_update: Tank):
    updated_tank = await db["tanks4"].update_one(
        {"_id": ObjectId(id)},
        {"$set": tank_update.model_dump(exclude_unset=True)},
    )

    if updated_tank.modified_count > 0:
        patched_tank = await db["tanks4"].find_one(
            {"_id": ObjectId(id)}
        )
        
        return Tank(**patched_tank)
    
    raise HTTPException(status_code = 404, detail = "Tank of id: " + id + " not found.")

@app.delete("/tank/{id}")
async def delete_tank(id: str):
    deleted_tank = await db["tanks4"].delete_one({"_id": ObjectId(id)})

    if deleted_tank.deleted_count < 1:
        raise HTTPException(status_code = 404, detail = "Tank of id: " + id + " not found.")
    
    return Response(status_code = 204)