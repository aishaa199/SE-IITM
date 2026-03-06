import os

from flask import Flask, render_template, request
from application.models import db
from application.sec import datastore
from flask_security import Security
from config import DevelopmentConfig
from upload_initial_data import seed_initial_data

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    
    # Initialize Security
    app.security = Security(app, datastore)
    
    with app.app_context():
        import application.views as views
        app.register_blueprint(views.main)
        db.create_all()
        seed_initial_data()
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
