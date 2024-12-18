import uuid
import os

class Config(object):
    
    # App Configurations
    SECRET_KEY =  uuid.uuid4().hex
    UPLOAD_DIR =  f'{os.getcwd()}/uploads'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024 * 1024
    FILE_EXPIRE_DURATION = 3600

    # SQLALCHEMY URI Configurations
    SQLALCHEMY_DATABASE_URI = 'sqlite:///file_share.db'


class Developement(Config):
    try:
        pass
    except Exception as e:
        print('Error generated in Developement Class:- ',e)