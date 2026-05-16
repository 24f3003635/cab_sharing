from app.factory import create_app
from app.database import db
from app.models import VehicleType

app = create_app()
if __name__ == "__main__":

    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully!")
            if VehicleType.query.count() == 0:
                vehicle_types = [
                    VehicleType(name="Auto", max_passengers=3),
                    VehicleType(name="Cab", max_passengers=4),
                    VehicleType(name="SUV", max_passengers=6),
                ]

            db.session.add_all(vehicle_types)
            db.session.commit()
            print("Vehicle types inserted.")

        except Exception as e:
            print(f"Error creating database: {e}")

    app.run(debug=True)
