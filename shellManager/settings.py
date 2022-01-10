from .common_settings import *  # pylint: disable=W0401


INSTALLED_APPS += [
    'line',
    'item',
    'otp',
    'delivery',
    'inventory',
]


try:
    from configs import *  # pylint: disable=W0401
except ImportError:
    pass

ACCESS_TOKEN = '9VBQke8sQrOq4GhNcRYvz8dZrxKGFhNdTxoSwfwyGGf'