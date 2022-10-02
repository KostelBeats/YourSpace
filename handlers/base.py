# handlers/base.py
# Routing and main logic of pages in YourPlace social network
# Based on ITVDN's social network creation webinars
# Made by 0xR from The 0x3L1tE
# 2022, Alexey Shaforostov Ilya Fatkin, Denis Panchenko, Russian University of Transport, УИБ-212

import hashlib
import random
import string

import aiohttp_jinja2

from aiohttp import web
from aiohttp_session import get_session

from models.user import User
from models.post import Post


class Index(web.View):

    @aiohttp_jinja2.template('index.html')
    async def get(self):
        conf = self.app['config']
        session = await get_session(self)
        user = {}
        posts = []
        friends = []
        if 'user' in session:
            posts = await Post.get_posts_by_user(db=self.app['db'], user_id=session['user']['_id'])
            friends = await User.get_user_friends(db=self.app['db'], user_id=session['user']['_id'])

        return dict(conf=conf, user=user, posts=posts, friends=friends)


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
            return web.HTTPNotFound()

        if user['password'] == hashlib.sha256(password.encode('utf8')).hexdigest():
            session = await get_session(self)
            session['user'] = user
            location = self.app.router['index'].url_for()
            return web.HTTPFound(location=location)

        return web.HTTPNotFound()


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
        del session['user']

        location = self.app.router['login'].url_for()
        return web.HTTPFound(location=location)


class Welcome(web.View):

        @aiohttp_jinja2.template('welcome.html')
        async def get(self):
            pass


class PostView(web.View):

    async def post(self):
        data = await self.post()
        print("Data keys: ", data.keys())
        session = await get_session(self)
        print("Session keys: ", session.keys())
        if 'user' in session and data['message'] and data['opr'] == 'c':
            await Post.create_post(db=self.app['db'], user_id=session['user']['_id'],
                                   message=data['message'], first_name=session['user']['first_name'],
                                   last_name=session['user']['last_name'])
            return web.HTTPFound(location=self.app.router['index'].url_for())

        if 'user' in session and data['opr'] == 'd':
            print("Post deletion in PostView")
            print("Post Base Data: ", data['post_id'])
            print("Reason: ", data['opr'])
            await Post.delete_post(db=self.app['db'], post_id=data['post_id'])
            return web.HTTPFound(location=self.app.router['index'].url_for())

        if 'user' in session and data['opr'] == 'e':
            print("Post editing in PostView")
            print("Post Base Data: ", data['post_id'])
            print("Reason: ", data['opr'])
            await Post.edit_post(db=self.app['db'], post_id=data['post_id'], message=data['message'])
            return web.HTTPFound(location=self.app.router['index'].url_for())

        return web.HTTPForbidden()
