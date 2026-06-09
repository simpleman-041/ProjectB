from flask import Flask,render_template, jsonify
from model import init_db
from route import create_route

def create_app():
    app = Flask(__name__)
    init_db(app)
    create_route(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
