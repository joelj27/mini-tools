class Config(object):
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER ="E:\study\word count\mini-tools\static\images"
    ALLOWED_EXTENSIONS = set(["png","jpg"])
    MONGO_URI = "mongodb://localhost:27017/website"
class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True