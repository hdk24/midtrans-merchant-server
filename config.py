from os import path, environ

basedir = path.abspath(path.dirname(__file__))


class Config:
    # common config
    SECRET_KEY = 'yKBeQa7iVu9GQibcic4h75jxzkjwU3O5Bagffe7FDg4'
    WTF_CSRF_ENABLED = False
    E500_ACTIVATED = False
    JSON_SORT_KEYS = False

    # database
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or 'sqlite:///' + path.join(basedir, 'midtrans.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # payment config
    PAYMENT_METHODS = []  # gopay, bca, bni, bri, permata


class ProductionConfig(Config):
    # common config
    E500_ACTIVATED = True

    # database
    SQLALCHEMY_DATABASE_URI = ""

    # payment config
    MIDTRANS_BASE_URL = "app.midtrans.com/v2"
    MIDTRANS_SERVER_KEY = ""
    MIDTRANS_CLIENT_KEY = ""
    PAYMENT_METHODS = ['gopay', 'bca']


class DevelopmentConfig(Config):
    # payment config
    MIDTRANS_BASE_URL = "https://api.sandbox.midtrans.com/v2"
    MIDTRANS_SERVER_KEY = ""
    MIDTRANS_CLIENT_KEY = ""
    PAYMENT_METHODS = ['gopay', 'bca', 'bri', 'bni', 'permata']


def load_config():
    mode = environ.get('FLASK_ENV')
    if mode == 'production':
        return ProductionConfig
    elif mode == 'development':
        return DevelopmentConfig
    else:
        return Config
