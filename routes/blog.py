# Imports
from fastapi import APIRouter
from models.blog import Blog
from config.database import collection_name
from schema.blog import list_serial
from bson import ObjectId

# Initialize 
router = APIRouter()

# GET Request Method
@router.get("/")
async def get_blogs():
    blogs = list_serial(collection_name.find())
    return blogs 

# POST Request Method
@router.post("/")
async def post_blog(blog: Blog):
    collection_name.insert_one(dict(blog))

# PUT Request Method
@router.put("/{id}")
async def edit_blog(id: str, blog: Blog):
    collection_name.find_one_and_update({"_id": ObjectId(id)},{
        "$set": dict(blog)
    }) 

# DELETE Request Method
@router.delete("/{id}")
async def delete_blog(id: str):
    collection_name.find_one_and_delete({"_id": ObjectId(id)})