import sys
import os

# Ensure the backend directory is in the path so we can import models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app, db
from application.models import SalonConfig

def upload_salon_config():
    with app.app_context():
        print("Starting salon configuration upload...")

        # Example Configurations
        configs = [
            {"param_name": "SALON_OPEN_TIME",            "param_value": "09:00"},
            {"param_name": "SALON_CLOSE_TIME",           "param_value": "21:00"},
            {"param_name": "REWARD_EXPIRY_DAYS",         "param_value": "180"},
            {"param_name": "POINTS_PER_CURRENCY",        "param_value": "0.1"},
            {"param_name": "VIP_POINTS_FOR_REDUMPTION",  "param_value": "500"},
            {"param_name": "REDUMPTION_VALUE_PER_POINT", "param_value": "0.05"},
            {"param_name": "FIRST_VISIT_BONUS_POINTS",   "param_value": "20"},
            {"param_name": "BIRTHDAY_BONUS_POINTS",      "param_value": "50"},
            {"param_name": "VIP_DISCOUNT_PERCENTAGE",    "param_value": "15"},
            {"param_name": "APPT_ID_FOR_ABSENCE",        "param_value": "99999999"},
            {"param_name": "ATTENDANCE_THRESHOLD_TIME",  "param_value": "10:30"},
            {"param_name": "APPT_HISTORY_RETENTION_DAYS","param_value": "120"},
        ]
        
        try:
            for item in configs:
                # Check if param already exists to avoid duplicates
                existing = SalonConfig.query.filter_by(param_name=item["param_name"]).first()
                if not existing:
                    new_config = SalonConfig(**item)
                    db.session.add(new_config)
                    print(f"Adding: {item['param_name']}")
                else:
                    print(f"Skipping: {item['param_name']} (already exists)")
            
            db.session.commit()
            print("Successfully completed salon configuration upload.")
        except Exception as e:
            db.session.rollback()
            print(f"Error during upload: {str(e)}")

if __name__ == "__main__":
    upload_salon_config()
