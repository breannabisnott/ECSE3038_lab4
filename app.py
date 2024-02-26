from datetime import datetime
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
    id: Optional[PyObjectId] = Field(alias = "_id", default = None)
    last_updated: Optional[str] = None
    username: Optional[str] = None
    role: Optional[str] = None
    color: Optional[str] = None

async def update_profile():
    current_time = datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p")
    
    profile_info = await db["profiles4"].find().to_list(1)
    
    db["profiles4"].update_one(
        {"_id": profile_info[0]["_id"]},
        {"$set": {"last_updated": current_time}},
    )

@app.get("/profile")
async def get_profile():
    profile = await db["profiles4"].find().to_list(1)
    return TypeAdapter(List[Profile]).validate_python(profile)

@app.post("/profile", status_code=201)
async def create_profile(profile: Profile):
    profile_check = await db["profiles4"].find().to_list(1)

    if len(profile_check) == 0:
        current_time = datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p")
        
        profile_info = profile.model_dump()
        profile_info["last_updated"] = current_time
        new_profile = await db["profiles4"].insert_one(profile_info)

        created_profile = await db["profiles4"].find_one({"_id": new_profile.inserted_id})
        return Profile(**created_profile)
    
    raise HTTPException(status_code = 400, detail = "Unable to create more than 1 profile")

@app.get("/tank")
async def get_tanks():
    tanks = await db["tanks4"].find().to_list(999)
    return TypeAdapter(List[Tank]).validate_python(tanks)

@app.get("/tank/{id}")
async def get_tank(id: str):
    tank = await db["tanks4"].find_one({"_id": ObjectId(id)})
    if tank is None:
        raise HTTPException(status_code = 404, detail = "Tank of id: " + id + " not found.")
    return Tank(**tank)

@app.post("/tank", status_code=201)
async def create_tank(tank: Tank):
    new_tank = await db["tanks4"].insert_one(tank.model_dump())
    created_tank = await db["tanks4"].find_one({"_id": new_tank.inserted_id})

    await update_profile()

    return Tank(**created_tank)

@app.patch("/tank/{id}", status_code=200)
async def update_tank(id: str, tank_update: Tank):
    updated_tank = await db["tanks4"].update_one(
        {"_id": ObjectId(id)},
        {"$set": tank_update.model_dump(exclude_unset=True)}
    )
    
    await update_profile()

    if updated_tank.modified_count > 0:
        patched_tank = await db["tanks4"].find_one(
            {"_id": ObjectId(id)}
        )
        
        return Tank(**patched_tank)
    
    raise HTTPException(status_code = 404, detail = "Tank of id: " + id + " not found.")

@app.delete("/tank/{id}", status_code=204)
async def delete_tank(id: str):
    deleted_tank = await db["tanks4"].delete_one({"_id": ObjectId(id)})
    await update_profile()

    if deleted_tank.deleted_count < 1:
        raise HTTPException(status_code = 404, detail = "Tank of id: " + id + " not found.")