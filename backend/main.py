import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request
from flask_cors import CORS
from flask_mail import Mail
from application.models import db
from application.sec import datastore
from flask_security import Security
from config import DevelopmentConfig
from upload_initial_data import seed_initial_data



def create_app():
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)
    app.config.from_object(DevelopmentConfig)
    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    mail = Mail(app)
    app.mail = mail
    
    # Initialize Security
    app.security = Security(app, datastore)
    
    with app.app_context():
        import application.views as views
        from application.resources import api as restful_api
        app.register_blueprint(views.main)
        restful_api.init_app(app)

        # create_all is idempotent — creates only tables that don't exist yet
        db_path = os.path.join(app.instance_path, 'sm_devdb.db')
        db_exists = os.path.exists(db_path)
        db.create_all()
        if not db_exists:
            seed_initial_data()
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)