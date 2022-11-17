# handlers/messages.py
# Message handler of YourPlace social network
# Based on ITVDN's social network creation webinars
# Made by 0xR from The 0x3L1tE
# 2022, Alexey Shaforostov Ilya Fatkin, Denis Panchenko, Russian University of Transport, УИБ-212

import aiohttp_jinja2
from aiohttp import web

from models.message import Message
from models.user import User


class MessageView(web.View):

    @aiohttp_jinja2.template('messages.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        friends = await User.get_user_friends(db=self.app['db'], user_id=self.session['user']['_id'])
        messages = await Message.get_chats(db=self.app['db'], user_id=self.session['user']['_id'],
                                           limit=1024, friends=friends)

        return dict(messages=messages)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        location = self.app.router['messages'].url_for()
        data = await self.post()
        print(data)

        if data['reason'] == 'd':
            await Message.delete_message(db=self.app['db'], message_id=data['message_id'])
            return web.HTTPFound(location=location)
        elif data['reason'] == 's':
            await Message.create_message(db=self.app['db'], from_user=self.session['user']['_id'],
                                         to_user=data['to_user'], message=data['message_text'])
        elif data['reason'] == 'e':
            pass

        # returing html page
        return web.HTTPFound(location=location)
