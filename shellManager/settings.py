from .common_settings import *  # pylint: disable=W0401


INSTALLED_APPS += [
    'line'
]


try:
    from configs import *  # pylint: disable=W0401
except ImportError:
    pass

access_token = 'oxCyrrgf1jWuQFU7c6yBghkJDmmRhmvvDNN6xTHlb5i'