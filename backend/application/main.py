from flask import Flask, render_template, request
from application.models import db
from application.sec import datastore
from flask_security import Security
from backend.config import DevelopmentConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    
    # Initialize Security
    app.security = Security(app, datastore)
    
    with app.app_context():
        import application.views as views
        app.register_blueprint(views.main)  
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
