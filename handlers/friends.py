# handlers/friends.py
# Friend system handler of YourPlace social network
# Based on ITVDN's social network creation webinars
# Made by 0xR from The 0x3L1tE
# 2022, Alexey Shaforostov Ilya Fatkin, Denis Panchenko, Russian University of Transport, УИБ-212

import aiohttp_jinja2
from aiohttp import web

from models.user import User


class FriendsView(web.View):

    @aiohttp_jinja2.template('friends_list.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['error_403'].url_for())

        users = await User.get_user_friends_suggestions(db=self.app['db'], user_id=self.session['user']['_id'])
        return dict(users=users)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['error_403'].url_for())

        data = await self.post()
        await User.add_friend(db=self.app['db'], user_id=self.session['user']['_id'], friend_id=data['uid'])
        location = self.app.router['friends'].url_for()
        return web.HTTPFound(location=location)


class UserFriends(web.View):

    @aiohttp_jinja2.template('friends.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['error_403'].url_for())

        users = await User.get_user_friends(db=self.app['db'], user_id=self.session['user']['_id'])

        return dict(friends=users)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['error_403'].url_for())
