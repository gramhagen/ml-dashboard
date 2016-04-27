# -*- coding: utf-8 -*-
"""Pytest setup """

import pytest

from application.app_factory import build_app
from application.models import db


@pytest.yield_fixture(scope="session")
def app():
    """Flask application fixture """
    _app = build_app(env='test')
    db.create_all()
    yield _app
    db.drop_all()
