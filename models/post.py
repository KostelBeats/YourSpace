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
    async def create_post(db: AsyncIOMotorDatabase, user_id: str, message: str, first_name: str, last_name: str):
        data = {
            'user_id': ObjectId(user_id),
            'message': message,
            'date_created': datetime.utcnow(),
            'author_first': first_name,
            'author_last': last_name
        }
        await db.posts.insert_one(data)

    # Get posts created by user
    # Inputs: Database, Author, Post count
    # Outputs: List of post objects, created by Author

    @staticmethod
    async def get_posts_by_user(db: AsyncIOMotorDatabase, user_id: str, limit=20):

        # user's posts
        user = await db.users.find_one({'_id': ObjectId(user_id)})

        # user friends' posts
        posts = await db.posts.find({'user_id': ObjectId(user_id)}).to_list(limit)

        # add string of user_id i every post
        for post in posts:
            post['str_user_id'] = str(post['user_id'])

        # list through every post by user's friends
        for friend in user['friends']:
            temp = await db.posts.find({'user_id': ObjectId(friend)}).to_list(limit)
            for post in temp:
                post['str_user_id'] = str(post['user_id'])
                posts.append(post)

        return posts


    # Edit post created by user
    # Inputs: Database, Post ID
    # Outputs: None. This method edits the post object in Database

    @staticmethod
    async def edit_post(db: AsyncIOMotorDatabase, post_id: str, message: str):
        await db.posts.update_one({'_id': ObjectId(post_id)}, {'$set': {'message': message}})


    # Delete post created by user
    # Inputs: Database, Post ID
    # Outputs: None. This method deletes post object from Database

    @staticmethod
    async def delete_post(db: AsyncIOMotorDatabase, post_id: str):
        await db.posts.delete_one({'_id': ObjectId(post_id)})
