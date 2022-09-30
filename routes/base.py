# /routes/base.py
# Routes of pages in YourPlace social network
# Based on ITVDN's social network creation webinars
# Made by 0xR from The 0x3L1tE
# 2022, Alexey Shaforostov Ilya Fatkin, Denis Panchenko, Russian University of Transport, УИБ-212

from handlers.base import Index, Login, Signup, Logout, PostView
from handlers.avatar import Avatar
from handlers.friends import FriendsView
from handlers.messages import MessageView

from config.common import BaseConfig


def setup_routes(app):
    app.router.add_get('/', Index.get, name='index')

    app.router.add_get('/login', Login.get, name='login')
    app.router.add_post('/login', Login.post)
    app.router.add_get('/signup', Signup.get, name='signup')
    app.router.add_post('/signup', Signup.post)
    app.router.add_get('/logout', Logout.get, name='logout')

    app.router.add_post('/save_avatar', Avatar.post, name='save_avatar')

    app.router.add_post('/add_post', PostView.post, name='add_post')

    app.router.add_get('/friends', FriendsView.get, name='friends')
    app.router.add_post('/add_friend', FriendsView.post, name='add_friend')

    app.router.add_get('/messages/{type}', MessageView.get, name='messages')
    app.router.add_post('/send_message', MessageView.post, name='send_message')


def setup_static_routes(app):
    app.router.add_static('/static/', path=BaseConfig.STATIC_DIR, name='static')
