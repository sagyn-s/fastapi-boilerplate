from datetime import datetime
from typing import Any

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, data: dict[str, Any]):
        data["user_id"] = ObjectId(user_id)
        data["created_at"] = datetime.utcnow()
        insert_result = self.database["shanyraks"].insert_one(data)
        return insert_result.inserted_id

    def get_shanyrak(self, shanyrak_id: str):
        return self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})
    
    def update_shanyrak(self, shanyrak_id: str, user_id: str, data: dict[str, Any]) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={
                "$set": data,
            },
        )
    
    def delete_shanyrak(self, shanyrak_id: str, user_id: str) -> DeleteResult:
        return self.database["shanyraks"].delete_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )
    
    def get_shanyraks(self, limit: int, offset: int, type: str, rooms_count: int, price_from: int, price_until: int, latitude: float, longitude: float, radius: float):
        query = {}
        if type is not None:
            query["type"] = {"$eq": type}
        if rooms_count is not None:
            query["rooms_count"] = {"$eq": rooms_count}
        if price_from is not None and price_until is not None:
            query["price"] = {"$gt": price_from,
                              "$lt": price_until}
        elif price_from is not None:
            query["price"] = {"$gt": price_from}
        elif price_until is not None:
            query["price"] = {"$lt": price_until}
        if latitude is not None:
            radius_converted_approximately = radius * 3.2535313808
            query["location"] = {
                "$geoWithin": {
                    "$centerSphere": [ [longitude, latitude], radius_converted_approximately ]
                }
            }

        total_count = self.database["shanyraks"].count_documents(query)
        
        cursor = self.database["shanyraks"].find(query).limit(limit).skip(offset).sort("created_at")
        result = []
        for item in cursor:
            result.append(item)
            
        return {
            "total": total_count,
            "objects": result
        }
