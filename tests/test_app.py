from fastapi import FastAPI
from wallet.app import app


def test_app_is_fastapi():
    assert isinstance(app, FastAPI)
