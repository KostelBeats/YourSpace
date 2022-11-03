# handlers/base.py
# Routing and main logic of pages in YourPlace social network
# Based on ITVDN's social network creation webinars
# Made by 0xR from The 0x3L1tE
# 2022, Alexey Shaforostov Ilya Fatkin, Denis Panchenko, Russian University of Transport, УИБ-212

import hashlib

import aiohttp_jinja2

from aiohttp import web
from aiohttp_session import get_session

from models.user import User


class Index(web.View):

    @aiohttp_jinja2.template('main.html')
    async def get(self):
        conf = self.app['config']
        session = await get_session(self)
        user = {}
        posts = []
        friends = []
        if 'user' in session:
            pass

        return dict(conf=conf, user=user, friends=friends)


class Login(web.View):

    @aiohttp_jinja2.template('login.html')
    async def get(self):
        return dict()

    async def post(self):
        data = await self.post()
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


