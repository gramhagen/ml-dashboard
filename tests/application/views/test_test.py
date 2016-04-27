# -*- coding: utf-8 -*-
"""Test example """


def test_test(client):
    assert client.get('test/').status_code == 200
