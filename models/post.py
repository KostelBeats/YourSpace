# models/post.py
# Model of Post in YourPlace social network
# Based on ITVDN's social network creation webinars
# Made by 0xR from The 0x3L1tE
# 2022, Alexey Shaforostov Ilya Fatkin, Denis Panchenko, Russian University of Transport, УИБ-212

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime


class Post:

    # Create post in feed
    # Inputs: Database, Author, Post message, Post ID
    # Outputs: Post object

    @staticmethod
    async def create_post(db: AsyncIOMotorDatabase, user_id: str, message: str):
        data = {
            'user_id': ObjectId(user_id),
            'message': message,
            'date_created': datetime.utcnow(),
        }
        await db.posts.insert_one(data)

    # Get posts created by user
    # Inputs: Database, Author, Post count
    # Outputs: List of post objects, created by Author

    @staticmethod
    async def get_posts_by_user(db: AsyncIOMotorDatabase, user_id: str, limit=20):
        posts = await db.posts.find({'user_id': ObjectId(user_id)}).to_list(limit)
        return posts

    # Edit post created by user
    # Inputs: Database, Author, Post ID
    # Outputs: Edited post object

    @staticmethod
    async def edit_post(db: AsyncIOMotorDatabase, user_id: str, date_time: str):
        pass

    # Delete post created by user
    # Inputs: Database, Author, Post ID
    # Outputs: None. This method deletes post object from Database

    @staticmethod
    async def delete_post(db: AsyncIOMotorDatabase, user_id: str, post_id: str):
        await db.posts.delete_one({'_id': ObjectId(post_id)})
