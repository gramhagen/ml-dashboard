# -*- coding: utf-8 -*-
"""WSGI app """

from src.app_factory import build_app


app = build_app()
