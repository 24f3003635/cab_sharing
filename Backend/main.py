from app.factory import create_app
from app.database import db

app = create_app()
if __name__ == '__main__':
    
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating database: {e}")
    
    app.run(debug=True)