import json
from app.db.session import SessionLocal
from app.models.medical_specialty import MedicalSpecialty

def seed():
    db = SessionLocal()
    with open("app/data/specialties.json", "r", encoding="utf-8") as f:
        specialties = json.load(f)

    for item in specialties:
        exists = db.query(MedicalSpecialty).filter_by(name=item["name"]).first()
        if not exists:
            db.add(MedicalSpecialty(**item))

    db.commit()
    db.close()
    print("Seeding completed.")

if __name__ == "__main__":
    seed()