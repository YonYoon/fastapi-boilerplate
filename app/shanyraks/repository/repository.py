from typing import Any

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, data: dict[str, Any]):
        data["user_id"] = ObjectId(user_id)
        insert_result = self.database["shanyraks"].insert_one(data)
        return insert_result.inserted_id

    def get_shanyrak(self, shanyrak_id: str):
        return self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})

    def update_shanyrak(
            self, shanyrak_id: str,
            user_id: str,
            data: dict[str, Any]
    ) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={
                "$set": data,
            }
        )

    def delete_shanyrak(self, shanyrak_id: str, user_id: str) -> DeleteResult:
        return self.database["shanyraks"].delete_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )

    def add_media(self, result: list, shanyrak_id: str):
        self.database["shanyraks"].update_one(
            {"_id": ObjectId(shanyrak_id)},
            {"$push": {"media": {"$each": result}}}
        )

    def delete_media(self, shanyrak_id: str):
        self.database["shanyraks"].update_one(
            {"_id": ObjectId(shanyrak_id)},
            {"$unset": {"media": 1}}
        )

    def add_comment(self,
                    shanyrak_id: str,
                    user_id: str,
                    data: str,
                    comment_id: str,
                    time: str):
        comment = {
            "_id": comment_id,
            "content": data,
            "created at": time,
            "author_id": user_id
        }

        self.database["shanyraks"].update_one(
            {"_id": ObjectId(shanyrak_id)},
            {"$push": {"comments": comment}}
        )
