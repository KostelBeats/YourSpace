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
        data = {
            'from_user': ObjectId(from_user),
            'to_user': ObjectId(to_user),
            'message': message,
            'author_first': author['first_name'],
            'author_last': author['last_name'],
            'date_created': datetime.utcnow(),
            'contents': [],
            'author_avatar_url': author['avatar_url']
        }

        await db.messages.insert_one(data)

    # Get list of sent messages in chat
    # Inputs: Database, User ID, List size
    # Outputs: List of sent messages

    @staticmethod
    async def get_chat(db: AsyncIOMotorDatabase, target_id: str, user_id: str, limit: int):

        # get inbox
        messages = await db.messages.find({'from_user': ObjectId(target_id),
                                           'to_user': ObjectId(user_id)}).to_list(limit)

        # get outbox
        messages += await db.messages.find({'from_user': ObjectId(user_id),
                                            'to_user': ObjectId(target_id)}).to_list(limit)

        # sort by date
        messages = sorted(
            messages,
            key=lambda x: (x['date_created'], '%Y-%m-%d %H:%M:%S'), reverse=False
        )
        return messages

    @staticmethod
    async def get_chats(db: AsyncIOMotorDatabase, user_id: str, limit: int, friends):

        messages = await db.messages.find({'from_user': ObjectId(target_id),
                                           'to_user': ObjectId(user_id)}).to_list(limit)

        # get outbox
        messages += await db.messages.find({'from_user': ObjectId(user_id),
                                            'to_user': ObjectId(target_id)}).to_list(limit)

        # sort by date
        messages = sorted(
            messages,
            key=lambda x: (x['date_created'], '%Y-%m-%d %H:%M:%S'), reverse=False
        )

        output = []
        for item in messages:
            if dict(message=item['messsage'], user_first=item['author_first'],
                    user_last=item['author_last'], date_created=item['date_created']) not in output:
                output.append(dict(message=item['messsage'], user_first=item['author_first'],
                                   user_last=item['author_last'], date_created=item['date_created']))

        return output

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
