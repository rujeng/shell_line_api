from .common_settings import *  # pylint: disable=W0401


INSTALLED_APPS += [
    'line',
    'item',
    'otp',
    'delivery',
]


try:
    from configs import *  # pylint: disable=W0401
except ImportError:
    pass

ACCESS_TOKEN = 'oxCyrrgf1jWuQFU7c6yBghkJDmmRhmvvDNN6xTHlb5i'