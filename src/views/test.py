# -*- coding: utf-8 -*-
"""Test page """

from flask import Blueprint, render_template


test = Blueprint('test', __name__, url_prefix='/')


@test.route('/')
def index():
    """ Test """
    return render_template('test/index.html')
