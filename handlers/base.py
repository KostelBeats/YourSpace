# handlers/base.py
# Routing and main logic of pages in YourPlace social network
# Based on ITVDN's social network creation webinars
# Made by 0xR from The 0x3L1tE
# 2022, Alexey Shaforostov Ilya Fatkin, Denis Panchenko, Russian University of Transport, УИБ-212

import hashlib
import bson
import aiohttp_jinja2

from aiohttp import web
from aiohttp_session import get_session

from models.user import User
from models.message import Message


class Index(web.View):

    @aiohttp_jinja2.template('main.html')
    async def get(self):
        conf = self.app['config']
        session = await get_session(self)
        print('index session', session)
        user = {}
        posts = []
        friends = []
        if 'user' in session:
            pass
        return dict(conf=conf, user=user, friends=friends)


class EditProfile(web.View):

    @aiohttp_jinja2.template('edit_profile.html')
    async def get(self):
        session = await get_session(self)
        if 'user' not in self.session:
            return web.HTTPForbidden()
        print(session['user'])
        return dict(user=session['user'])

    async def post(self):
        session = await get_session(self)
        if 'user' not in self.session:
            return web.HTTPForbidden()

        data = await self.post()
        if data['edit_type'] == '0':
            await User.edit_main(db=self.app['db'], user_id=session['user']['_id'], data=data)
        elif data['edit_type'] == '1':
            await User.edit_sec(db=self.app['db'], user_id=session['user']['_id'], data=data)

        location = self.app.router['index'].url_for()
        return web.HTTPFound(location=location)


class Profile(web.View):
    @aiohttp_jinja2.template('profile.html')
    async def get(self):
        session = await get_session(self)
        if 'user' not in session:
            return web.HTTPFound(location=self.app.router['error_403'].url_for())

        # WTF? HTTP/get is stupid!
        # getting the uid from url
        # split str(url) to host/page, unfiltered data
        # take unfiltered data from split array and split it in unfiltered chunks
        # take unfiltered chunk with t_profile and split it to text, val
        # take val with uid and process it further
        # Fuck you, HTTP!

        data = str(self.url).split("?")[1].split("&x")[0].split("t_profile=")[1]

        # try to find user in db...

        try:
            tu = await User.get_user_by_id(db=self.app['db'], user_id=data)
        except bson.errors.InvalidId:
            return web.HTTPFound(location=self.app.router['error_403'].url_for())

        return dict(user=tu)


class Login(web.View):

    @aiohttp_jinja2.template('login.html')
    async def get(self):
        session = await get_session(self)
        print('get login session', session)

        return dict()

    async def post(self):
        data = await self.post()
        session = await get_session(self)
        print('post login session', session)
        email = data['email']
        password = data['password']
        user = await User.get_user_by_email(db=self.app['db'], email=email)
        if user.get('error'):
            return web.HTTPFound(location=self.app.router['error_404'].url_for())

        if user['password'] == hashlib.sha256(password.encode('utf8')).hexdigest():
            session = await get_session(self)
            session['user'] = user
            location = self.app.router['index'].url_for()
            return web.HTTPFound(location=location)

        return web.HTTPFound(location=self.app.router['error_404'].url_for())


class Signup(web.View):

    @aiohttp_jinja2.template('signup.html')
    async def get(self):
        return dict()

    async def post(self):
        data = await self.post()
        result = await User.create_new_user(db=self.app['db'], data=data)
        if not result:
            # todo: show error on ui!
            location = self.app.router['signup'].url_for()
            return web.HTTPFound(location=location)

        location = self.app.router['login'].url_for()
        return web.HTTPFound(location=location)


class Logout(web.View):

    async def get(self):
        session = await get_session(self)
        if 'user' in session:
            del session['user']

        else:
            return web.HTTPForbidden()

        location = self.app.router['login'].url_for()
        return web.HTTPFound(location=location)


class Welcome(web.View):

    @aiohttp_jinja2.template('welcome.html')
    async def get(self):
        pass


class Error404(web.View):

    @aiohttp_jinja2.template('error_404.html')
    async def get(self):
        pass


class Error403(web.View):

    @aiohttp_jinja2.template('error_403.html')
    async def get(self):
        pass


class Error500(web.View):

    @aiohttp_jinja2.template('error_500.html')
    async def get(self):
        pass


class Chat(web.View):

    @aiohttp_jinja2.template('chat.html')
    async def get(self):
        session = await get_session(self)

        if 'user' not in session:
            return web.HTTPFound(location=self.app.router['error_403'].url_for())
        # WTF? HTTP/get is stupid!
        # getting the uid from url
        # split str(url) to host/page, unfiltered data
        # take unfiltered data from split array and split it in unfiltered chunks
        # take unfiltered chunk with t_profile and split it to text, val
        # take val with uid and process it further
        # Fuck you, HTTP!

        target_id = str(self.url).split("?")[1].split("&x")[0].split("t_profile=")[1]
        session = await get_session(self)
        target = await User.get_user_by_id(db=self.app['db'], user_id=target_id)
        messages = await Message.get_chat(db=self.app['db'], user_id=session['user']['_id'],
                                          target_id=target_id, limit=1024)
        print(session)

        return dict(current_user=session['user'], target_user=target, messages=messages)

    async def post(self):
        pass