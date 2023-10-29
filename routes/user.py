# Imports
from fastapi import APIRouter
from models.user import User
from config.database import collection_name
from schema.user import list_serial
from bson import ObjectId

# Initialize 
router = APIRouter()

# GET Request Method
@router.get("/users")
async def get_users():
    users = list_serial(collection_name.find())
    return users 

# POST Request Method
@router.post("/users")
async def post_user(user: User):
    collection_name.insert_one(dict(user))

# PUT Request Method
@router.put("/{id}")
async def edit_user(id: str, user: User):
    collection_name.find_one_and_update({"_id": ObjectId(id)},{
        "$set": dict(user)
    })

# DELETE Request Method
@router.delete("/{id}")
async def delete_user(id: str):
    collection_name.find_one_and_delete({"_id": ObjectId(id)})