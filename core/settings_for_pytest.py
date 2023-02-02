from core.base_settings import *  # noqa
import os

# pytst-djangoでは自動でDEBUG=Falseになるのでテスト関数でsettings.DEBUG = Falseとする
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))),
            'test_db.sqlite3'),
    }
}
