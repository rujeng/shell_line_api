from .common_settings import *  # pylint: disable=W0401


INSTALLED_APPS += [
    'line',
    'item',
    'otp',
    'delivery',
    'inventory',
]

MIDDLEWARE += [
    'delivery.middlewares.activatetime_middleware.ActivatetimeMiddleware'
]
LOGIN_URL = '../../user/login'

try:
    from configs import *  # pylint: disable=W0401
except ImportError:
    pass

ACCESS_TOKEN = '9VBQke8sQrOq4GhNcRYvz8dZrxKGFhNdTxoSwfwyGGf'