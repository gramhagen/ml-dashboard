# -*- coding: utf-8 -*-
# pylint: disable=E1101,R0204
"""Flask app """

import logging
import os
import sys
from flask import Flask
from flask_iniconfig import INIConfig

from .models import db
from .views import blueprints


def build_app(env=None):
    """Application Factory

    Args:
        env (str) : set configuration environment [dev|test|prod], default = dev
    Returns:
        (object) : Flask application
    """
    app = Flask(__name__)

    # most manage.py tasks don't need a fully configured app
    if 'manage.py' in sys.argv:
        if sys.argv[-1] not in ['runserver', 'test']:
            return app

    # set configuration environment
    if not env:
        env = os.getenv('ENV', 'dev')

    # configure app
    INIConfig(app)
    ini_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'instance', 'flask.ini')
    if not os.path.exists(ini_file):
        raise IOError('Could not open: {}, create Flask ini file using `python manage.py init`'.format(ini_file))
    app.config.from_inifile_sections(ini_file, ['common', env])

    # configure logging
    try:
        handler = logging.FileHandler(app.config['LOG_PATH'])
    except KeyError:
        handler = logging.StreamHandler()
    handler.setFormatter(fmt=logging.Formatter(fmt=app.config.get('LOG_FMT')))
    app.logger.addHandler(handler)
    app.logger.setLevel(level=logging.getLevelName(app.config.get('LOG_LEVEL', logging.DEBUG)))

    # init sqlalchemy database
    db.init_app(app)

    # register blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    app.logger.debug('created flask app using %s environment', env)

    return app
