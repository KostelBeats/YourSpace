# models/user.py
# Model of User in YourPlace social network
# Based on ITVDN's social network creation webinars
# Made by 0xR from The 0x3L1tE
# 2022, Alexey Shaforostov Ilya Fatkin, Denis Panchenko, Russian University of Transport, УИБ-212

import hashlib
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class User:

    # Find user in database by its email
    # Inputs: Database, Email
    # Outputs: User object from Database

    @staticmethod
    async def get_user_by_email(db: AsyncIOMotorDatabase, email: str):
        user = await db.users.find_one({'email': email})

        if user:
            user['_id'] = str(user['_id'])
            user['friends'] = [str(uid) for uid in user['friends']]
            return user
        else:
            return dict(error='User with email {} not found'.format(email))

    # Find user in database by its id
    # Inputs: Database, Email
    # Outputs: User object from Database

    @staticmethod
    async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: str):
        user = await db.users.find_one({'_id': ObjectId(user_id)})
        # print("get_user_by_id: ", user.keys())
        if user:
            user['_id'] = str(user['_id'])
            user['friends'] = [str(uid) for uid in user['friends']]
            return user
        else:
            return None

    # Create new user in database
    # Inputs: Database, First name, Last name, Email, Password
    # Outputs: User object

    @staticmethod
    async def create_new_user(db: AsyncIOMotorDatabase, data):
        email = data['email']
        nickname = data['nickname']
        user = await db.users.find_one({'email': email})
        if user:
            return dict(error='user with email {} exist'.format(email))

        if data['first_name'] and data['last_name'] and data['password']:
            data = dict(data)
            data['password'] = hashlib.sha256(data['password'].encode('utf8')).hexdigest()
            data['friends'] = []
            data['friends_approval'] = []
            data['location'] = 'не указано'
            data['age'] = 'не указан'
            data['work'] = 'не указано'
            data['bio'] = 'пустой статус'
            result = await db.users.insert_one(data)
            return result
        else:
            return dict(error='Missing user data parameters')

    # Save user's avatar
    # Inputs: Database, User ID, URL to photo
    # Outputs: None. This method updates / sets URL in Database

    @staticmethod
    async def save_avatar_url(db: AsyncIOMotorDatabase, user_id: str, url: str):
        if url and user_id:
            db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'avatar_url': url}})

    # Get possible friends list (mutual friends)
    # Inputs: Database, User ID, List size
    # Outputs: List of mutual or possible friends

    @staticmethod
    async def get_user_friends_suggestions(db: AsyncIOMotorDatabase, user_id: str, limit=1024):
        query = {'_id': {'$ne': ObjectId(user_id)}}
        users = await db.users.find(query).to_list(limit)
        return users

    # send request for adding a friend
    # Inputs: Database, User ID, Target ID
    # Outputs: None. This function sends request of friend list addition

    @staticmethod
    async def add_friend(db: AsyncIOMotorDatabase, user_id: str, friend_id: str):
        await db.users.update_one({'_id': ObjectId(user_id)}, {'$addToSet': {'friends_approval': ObjectId(friend_id)}})

    @staticmethod
    async def edit_main(db: AsyncIOMotorDatabase, user_id: str, data):
        if data['new_pass'] == data['passcheck']:
            await db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'first_name': data['first_name']}})
            await db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'last_name': data['last_name']}})
            await db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'email': data['email']}})
            await db.users.update_one({'_id': ObjectId(user_id)},
                                      {'$set': {
                                          'password': hashlib.sha256(data['new_pass'].encode('utf8')).hexdigest()}})
            return 0

        return -1

    @staticmethod
    async def edit_sec(db: AsyncIOMotorDatabase, user_id: str, data):
        await db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'location': data['location']}})
        await db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'work': data['work']}})
        await db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'age': data['age']}})
        await db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'nickname': data['nickname']}})
        await db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'bio': data['bio']}})
        return 0

    # Approve friend request
    # Inputs: Database, User ID, Target ID
    # Outputs: None. This function approves friend requests in Database

    @staticmethod
    async def friend_allow(db: AsyncIOMotorDatabase, user_id: str, friend_id: str):
        await db.users.update_one({'_id': ObjectId(user_id)}, {'$addToSet': {'friends': ObjectId(friend_id)}})
        await db.users.update_one({'_id': ObjectId(user_id)}, {'$pull': {'friends_approval': ObjectId(friend_id)}})
        await db.users.update_one({'_id': ObjectId(friend_id)}, {'$addToSet': {'friends': ObjectId(user_id)}})

    # Remove friend back to approval state
    # Inputs: Database, User ID, Target ID
    # Outputs: None. This function recalls friend requests approvals.

    @staticmethod
    async def friend_remove(db: AsyncIOMotorDatabase, user_id: str, friend_id: str):
        await db.users.update_one({'_id': ObjectId(user_id)}, {'$addToSet': {'friends_approval': ObjectId(friend_id)}})
        await db.users.update_one({'_id': ObjectId(user_id)}, {'$pull': {'friends': ObjectId(friend_id)}})
        await db.users.update_one({'_id': ObjectId(friend_id)}, {'$pull': {'friends': ObjectId(user_id)}})

    # Get list of user's friends
    # Inputs: Database, User ID, List size
    # Outputs: List of user's friends

    @staticmethod
    async def get_user_friends(db: AsyncIOMotorDatabase, user_id: str, limit=1024):
        user = await db.users.find_one({'_id': ObjectId(user_id)})
        user_friends = await db.users.find({'_id': {'$in': user['friends']}}).to_list(limit)
        return user_friends

    @staticmethod
    async def get_user_allow_list(db: AsyncIOMotorDatabase, user_id: str, limit=1024):
        user = await db.users.find_one({'_id': ObjectId(user_id)})
        user_friends = await db.users.find({'_id': {'$in': user['friends_approval']}}).to_list(limit)
        return user_friends

    # Add particular user to blacklist
    # Inputs: Database, User ID, Target ID
    # Outputs: None. This function adds Target ID to user's blacklist and
    # removes it from user's friend / friend approval list
