from fastapi import FastAPI

from common.post_construct import post_construct


app = FastAPI()

post_construct(app)
