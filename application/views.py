from flask import Blueprint

main = Blueprint('main', __name__)

@main.get('/')
def home():
    return "hello world"