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

class colours(BaseModel):
    aliceblue: Optional[str] = "#f0f8ff",
    antiquewhite: Optional[str] ="#faebd7",
    aqua: Optional[str] = "#00ffff",
    aquamarine: Optional[str] ="#7fffd4",
    azure: Optional[str] ="#f0ffff",
    beige: Optional[str] ="#f5f5dc",
    bisque: Optional[str] ="#ffe4c4",
    black: Optional[str] ="#000000",
    blanchedalmond: Optional[str] ="#ffebcd",
    blue: Optional[str] ="#0000ff",
    blueviolet: Optional[str] ="#8a2be2",
    brown: Optional[str] ="#a52a2a",
    burlywood: Optional[str] ="#deb887",
    cadetblue: Optional[str] ="#5f9ea0",
    chartreuse: Optional[str] ="#7fff00",
    chocolate: Optional[str] ="#d2691e",
    coral: Optional[str] ="#ff7f50",
    cornflowerblue: Optional[str] ="#6495ed",
    cornsilk:Optional[str] = "#fff8dc",
    crimson: Optional[str] ="#dc143c",
    cyan: Optional[str] ="#00ffff",
    darkblue: Optional[str] ="#00008b",
    darkcyan:Optional[str] = "#008b8b",
    darkgoldenrod:Optional[str] = "#b8860b",
    darkgray: Optional[str] ="#a9a9a9",
    darkgreen: Optional[str] ="#006400",
    darkkhaki: Optional[str] ="#bdb76b",
    darkmagenta: Optional[str] ="#8b008b",
    darkolivegreen:Optional[str] = "#556b2f",
    darkorange:Optional[str] = "#ff8c00",
    darkorchid:Optional[str] = "#9932cc",
    darkred: Optional[str] ="#8b0000",
    darksalmon: Optional[str] ="#e9967a",
    darkseagreen: Optional[str] ="#8fbc8f",
    darkslateblue:Optional[str] = "#483d8b",
    darkslategray:Optional[str] = "#2f4f4f",
    darkturquoise:Optional[str] = "#00ced1",
    darkviolet:Optional[str] = "#9400d3",
    deeppink:Optional[str] = "#ff1493",
    deepskyblue: Optional[str] ="#00bfff",
    dimgray: Optional[str] ="#696969",
    dodgerblue:Optional[str] = "#1e90ff",
    firebrick: Optional[str] ="#b22222",
    floralwhite: Optional[str] ="#fffaf0",
    forestgreen: Optional[str] ="#228b22",
    fuchsia: Optional[str] ="#ff00ff",
    gainsboro: Optional[str] ="#dcdcdc",
    ghostwhite: Optional[str] ="#f8f8ff",
    gold: Optional[str] ="#ffd700",
    goldenrod:Optional[str] = "#daa520",
    gray:Optional[str] = "#808080",
    green:Optional[str] = "#008000",
    greenyellow:Optional[str] = "#adff2f",
    honeydew:Optional[str] = "#f0fff0",
    hotpink: Optional[str] ="#ff69b4",
    indianred: Optional[str] ="#cd5c5c",
    indigo: Optional[str] ="#4b0082",
    ivory: Optional[str] ="#fffff0",
    khaki: Optional[str] ="#f0e68c",
    lavender: Optional[str] ="#e6e6fa",
    lavenderblush:Optional[str] = "#fff0f5",
    lawngreen:Optional[str] = "#7cfc00",
    lemonchiffon: Optional[str] ="#fffacd",
    lightblue: Optional[str] ="#add8e6",
    lightcoral:Optional[str] = "#f08080",
    lightcyan: Optional[str] ="#e0ffff",
    lightgoldenrodyellow: Optional[str] ="#fafad2",
    lightgrey: Optional[str] ="#d3d3d3",
    lightgreen: Optional[str] ="#90ee90",
    lightpink:Optional[str] = "#ffb6c1",
    lightsalmon:Optional[str] = "#ffa07a",
    lightseagreen:Optional[str] = "#20b2aa",
    lightskyblue: Optional[str] ="#87cefa",
    lightslategray: Optional[str] ="#778899",
    lightsteelblue:Optional[str] = "#b0c4de",
    lightyellow: Optional[str] ="#ffffe0",
    lime:Optional[str] = "#00ff00",
    limegreen:Optional[str] = "#32cd32",
    linen:Optional[str] = "#faf0e6",
    magenta: Optional[str] ="#ff00ff",
    maroon: Optional[str] ="#800000",
    mediumaquamarine: Optional[str] ="#66cdaa",
    mediumblue: Optional[str] ="#0000cd",
    mediumorchid:Optional[str] = "#ba55d3",
    mediumpurple:Optional[str] = "#9370d8",
    mediumseagreen: Optional[str] ="#3cb371",
    mediumslateblue: Optional[str] ="#7b68ee",
    mediumspringgreen: Optional[str] ="#00fa9a",
    mediumturquoise:Optional[str] = "#48d1cc",
    mediumvioletred:Optional[str] = "#c71585",
    midnightblue: Optional[str] ="#191970",
    mintcream:Optional[str] = "#f5fffa",
    mistyrose:Optional[str] = "#ffe4e1",
    moccasin:Optional[str] = "#ffe4b5",
    navajowhite:Optional[str] = "#ffdead",
    navy:Optional[str] = "#000080",
    oldlace:Optional[str] = "#fdf5e6",
    olive: Optional[str] ="#808000",
    olivedrab: Optional[str] ="#6b8e23",
    orange:Optional[str] = "#ffa500",
    orangered: Optional[str] ="#ff4500",
    orchid:Optional[str] = "#da70d6",
    palegoldenrod: Optional[str] ="#eee8aa",
    palegreen: Optional[str] ="#98fb98",
    paleturquoise:Optional[str] = "#afeeee",
    palevioletred:Optional[str] = "#d87093",
    papayawhip:Optional[str] = "#ffefd5",
    peachpuff: Optional[str] ="#ffdab9",
    peru: Optional[str] ="#cd853f",
    pink: Optional[str] ="#ffc0cb",
    plum:Optional[str] = "#dda0dd",
    powderblue: Optional[str] ="#b0e0e6",
    purple: Optional[str] ="#800080",
    rebeccapurple: Optional[str] ="#663399",
    red:Optional[str] = "#ff0000",
    rosybrown: Optional[str] ="#bc8f8f",
    royalblue: Optional[str] ="#4169e1",
    saddlebrown:Optional[str] = "#8b4513",
    salmon: Optional[str] ="#fa8072",
    sandybrown: Optional[str] ="#f4a460",
    seagreen: Optional[str] ="#2e8b57",
    seashell:Optional[str] = "#fff5ee",
    sienna:Optional[str] = "#a0522d",
    silver:Optional[str] ="#c0c0c0",
    skyblue:Optional[str] = "#87ceeb",
    slateblue:Optional[str] = "#6a5acd",
    slategray:Optional[str] = "#708090",
    snow:Optional[str] = "#fffafa",
    springgreen: Optional[str] ="#00ff7f",
    steelblue: Optional[str] ="#4682b4",
    tan:Optional[str] = "#d2b48c",
    teal: Optional[str] ="#008080",
    thistle: Optional[str] ="#d8bfd8",
    tomato:Optional[str] = "#ff6347",
    turquoise: Optional[str] ="#40e0d0",
    violet: Optional[str] ="#ee82ee",
    wheat: Optional[str] ="#f5deb3",
    white: Optional[str] ="#ffffff",
    whitesmoke: Optional[str] ="#f5f5f5",
    yellow: Optional[str] ="#ffff00",
    yellowgreen:Optional[str] = "#9acd32"

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

@app.patch("/tank/{id}")
async def update_tank(id: str, tank_update: Tank):
    updated_tank = await db["tanks4"].update_one(
        {"_id": ObjectId(id)},
        {"$set": tank_update.model_dump(exclude_unset=True)},
    )
    await update_profile()

    if updated_tank.modified_count > 0:
        patched_tank = await db["tanks4"].find_one(
            {"_id": ObjectId(id)}
        )
        
        return Tank(**patched_tank)
    
    raise HTTPException(status_code = 404, detail = "Tank of id: " + id + " not found.")

@app.delete("/tank/{id}")
async def delete_tank(id: str):
    deleted_tank = await db["tanks4"].delete_one({"_id": ObjectId(id)})
    await update_profile()

    if deleted_tank.deleted_count < 1:
        raise HTTPException(status_code = 404, detail = "Tank of id: " + id + " not found.")
    
    return Response(status_code = 204)