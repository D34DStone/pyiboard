import sys
import os

class Config:

    PROJECT_ROOT_DIR = os.path.dirname( os.path.abspath(__file__) )
    RESOURCES_DIR = os.path.join(PROJECT_ROOT_DIR, 'resources')
    PUBLIC_DIR = os.path.join(RESOURCES_DIR, 'public')
    UPLOAD_DIR = os.path.join(RESOURCES_DIR, 'uploads')
    TEMPLATES_DIR = os.path.join(PROJECT_ROOT_DIR, 'templates')
    VAR_DIR = os.path.join(PROJECT_ROOT_DIR, 'var')
    
    FILES_ROUTE = '/files/'
    PUBLIC_FILES_ROUTE = FILES_ROUTE + 'public/'
    AUDIO_FILES_PREVIEWS_ROUTE = PUBLIC_FILES_ROUTE + 'board-images/music-preview.png' 

    SALT = 'VfXR7TaGqF34bj1Z'
    HOST = 'localhost'
    PORT = 5000
    URL = 'localhost:5000'

    MUSIC_RREVIEW_PATH = os.path.join(os.path.join(PUBLIC_DIR, 'board-images'), 'music-preview.png')
    
    FLASK_CONFIG = {
        'TESTING': True, 
        'FLASK_ENV': "development",
        'TEMPLATES_AUTO_RELOAD': True,
        'DEBUG': True,
        'UPLOAD_FOLDER': UPLOAD_DIR,

        'SQLALCHEMY_DATABASE_URI': 'sqlite:///%s' % os.path.join(VAR_DIR, 'database.sqlite'),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }
