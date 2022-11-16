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
        if data['opr_type'] == 'add':
            await User.add_friend(db=self.app['db'], user_id=data['uid'], friend_id=self.session['user']['_id'])
        elif data['opr_type'] == 'apr':
            await User.friend_allow(db=self.app['db'], user_id=self.session['user']['_id'], friend_id=data['uid'])
        elif data['opr_type'] == 'del':
            await User.friend_remove(db=self.app['db'], user_id=self.session['user']['_id'], friend_id=data['uid'])
        location = self.app.router['friends'].url_for()
        return web.HTTPFound(location=location)


class UserFriends(web.View):

    @aiohttp_jinja2.template('friends.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['error_403'].url_for())

        to_allow = await User.get_user_allow_list(db=self.app['db'], user_id=self.session['user']['_id'])
        friends = await User.get_user_friends(db=self.app['db'], user_id=self.session['user']['_id'])

        return dict(allowlist=to_allow, friends=friends)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['error_403'].url_for())
