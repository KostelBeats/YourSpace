# handlers/messages.py
# Message handler of YourPlace social network
# Based on ITVDN's social network creation webinars
# Made by 0xR from The 0x3L1tE
# 2022, Alexey Shaforostov Ilya Fatkin, Denis Panchenko, Russian University of Transport, УИБ-212

import aiohttp_jinja2
from aiohttp import web

from models.message import Message


class MessageView(web.View):

    @aiohttp_jinja2.template('messages.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        messages = await Message.get_inbox_messages_by_user(db=self.app['db'], user_id=self.session['user']['_id'])

        return dict(messages=messages)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        data = await self.post()
        print(data)
        await Message.create_message(db=self.app['db'], from_user=self.session['user']['_id'],
                                     to_user=data['to_user'], message=data['message_text'])

        location = self.app.router['index'].url_for()
        return web.HTTPFound(location=location)
