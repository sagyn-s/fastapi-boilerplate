from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from fastapi import HTTPException
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult


class FavouritesRepository:
    def __init__(self, database: Database):
        self.database = database

    def add_to_favourite(self, shanyrak_id: str, user_id: str):
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})
        if not shanyrak:
            raise HTTPException(status_code=404, detail=f"Could find shanyrak with id {shanyrak_id}")
        payload = {}
        payload["user_id"] = ObjectId(user_id)
        payload["shanyrak_id"] = ObjectId(shanyrak_id)
        payload["address"] = shanyrak["address"]
        self.database["favourites"].insert_one(payload)
    
    def get_favourites(self, user_id: str) -> List[dict]:
        favourites = self.database["favourites"].find({"user_id": ObjectId(user_id)})
        return list(favourites)
    
    def delete_favourite(self, shanyrak_id: str, user_id: str) -> DeleteResult:
        return self.database["favourites"].delete_one(
            {"shanyrak_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )