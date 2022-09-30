# config/common.py
# Initial config of YourPlace social network
# Based on ITVDN's social network creation webinars
# Made by 0xR from The 0x3L1tE
# 2022, Alexey Shaforostov Ilya Fatkin, Denis Panchenko, Russian University of Transport, УИБ-212

import pathlib


class BaseConfig:

    debug = True
    app_name = 'YourPlace'
    secret_key = b'TyzLMReLCWUiPsTFMActw_0dtEU7kAcFXHNYYm64DNI='
    database_name = 'my_database'

    PROJECT_ROOT = pathlib.Path(__file__).parent.parent
    STATIC_DIR = str(PROJECT_ROOT / 'static')
