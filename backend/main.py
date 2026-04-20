import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request
from flask_cors import CORS
from flask_mail import Mail
from flask_apscheduler import APScheduler
from application.models import db
from application.sec import datastore
from flask_security import Security
from config import DevelopmentConfig
from upload_initial_data import seed_initial_data


scheduler = APScheduler()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)
    app.config.from_object(DevelopmentConfig)
    if test_config:
        app.config.update(test_config)
    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    mail = Mail(app)
    app.mail = mail

    # Initialize Scheduler
    if not scheduler.running:
        scheduler.init_app(app)
        # Store app reference in scheduler for tasks to use
        scheduler.app = app
        scheduler.start()

    # Initialize Security
    app.security = Security(app, datastore)
    
    # Update attendance job time from Database dynamically
    with app.app_context():
        # create_all is idempotent — creates only tables that don't exist yet
        db_path = os.path.join(app.instance_path, 'sm_devdb.db')
        db_exists = os.path.exists(db_path)
        db.create_all()
        if not db_exists:
            seed_initial_data()
            from upload_salon_config import upload_salon_config
            upload_salon_config()


        from application.models import SalonConfig
        threshold = SalonConfig.query.filter_by(param_name='ATTENDANCE_THRESHOLD_TIME').first()
        if threshold and ":" in threshold.param_value:
            try:
                h, m = map(int, threshold.param_value.split(":"))
                # Add 1 minute to the threshold
                m += 1
                if m >= 60:
                    m = 0
                    h = (h + 1) % 24
                
                # Reschedule the job specifically using the scheduler's API
                # This ensures the running scheduler instance is updated correctly.
                scheduler.add_job(
                    id='attendance_threshold_job',
                    func='application.tasks:mark_absent_staff',
                    trigger='cron',
                    hour=h,
                    minute=m,
                    replace_existing=True
                )
                print(f"Scheduler: Attendance job dynamically re-configured for {h:02d}:{m:02d} UTC")
            except Exception as e:
                print(f"Scheduler: Failed to dynamically update job: {str(e)}")
    
    with app.app_context():
        import application.views as views
        from application.resources import api as restful_api
        app.register_blueprint(views.main)
        restful_api.init_app(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)