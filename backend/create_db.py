from src.main import app, db
import os

# Remove existing database file if it exists
if os.path.exists("src/database/app.db"):
    os.remove("src/database/app.db")

with app.app_context():
    db.create_all()
    print("Database recreated successfully.")

