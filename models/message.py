# models/message.py
# Model of Message in YourPlace social network
# Based on ITVDN's social network creation webinars
# Made by 0xR from The 0x3L1tE
# 2022, Alexey Shaforostov Ilya Fatkin, Denis Panchenko, Russian University of Transport, УИБ-212

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime


class Message:

    # Create message object and send it
    # Inputs: Database, Author, Recipient, Message, Message ID
    # Outputs: None. This function sends message to Recipient

    @staticmethod
    async def create_message(db: AsyncIOMotorDatabase, from_user: str, to_user: str, message: str):
        author = await db.users.find_one({'_id': ObjectId(from_user)})
        recipient = await db.users.find_one({'_id': ObjectId(to_user)})
        data = {
            'from_user': ObjectId(from_user),
            'str_from_user': from_user,
            'str_to_user': to_user,
            'to_user': ObjectId(to_user),
            'message': message,
            'author_first' : author['first_name'],
            'author_last' : author['last_name'],
            'recipient_first' : recipient['first_name'],
            'recipient_last' : recipient['last_name'],
            'date_created': datetime.utcnow()
        }

        await db.messages.insert_one(data)

    # Get list of inbox messages
    # Inputs: Database, User ID, List size
    # Outputs: List of incoming messages

    @staticmethod
    async def get_inbox_messages_by_user(db: AsyncIOMotorDatabase, user_id: str, limit=20):

        messages_from = await db.messages.find({'from_user': ObjectId(user_id)}).to_list(limit)
        messages_to = await db.messages.find({'to_user': ObjectId(user_id)}).to_list(limit)

        return messages_to + messages_from

    # Get list of sent messages
    # Inputs: Database, User ID, List size
    # Outputs: List of sent messages

    @staticmethod
    async def get_send_messages_by_user(db: AsyncIOMotorDatabase, user_id: str, limit=20):
        messages = await db.messages.find({'from_user': ObjectId(user_id)}).to_list(limit)
        return messages

    # Edit message sent by user
    # Inputs: Database, Author, Message ID, Message
    # Outputs: None. This function edits message in Database

    @staticmethod
    async def edit_message(db: AsyncIOMotorDatabase, user_id: str, message_id: str, message: str):
        pass

    # Delete message sent by user
    # Inputs: Database, Author, Message ID, Message
    # Outputs: None. This function deletes message in Database

    @staticmethod
    async def delete_message(db: AsyncIOMotorDatabase, message_id: str):
        await db.messages.delete_one({'_id': ObjectId(message_id)})
