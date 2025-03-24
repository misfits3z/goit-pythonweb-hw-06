import random
from faker import Faker
from database import SessionLocal
from models import Student, Group, Teacher, Subject, Grade
from datetime import date, timedelta

fake = Faker()
db = SessionLocal()

# Створення груп
groups = [Group(name=f"Group {i}") for i in range(1, 4)]
db.add_all(groups)
db.commit()  

# Створення викладачів
teachers = [Teacher(full_name=fake.name()) for _ in range(4)]
db.add_all(teachers)
db.commit()  

# Створення предметів
subjects = [
    Subject(title="Mathematics", teacher_id=random.choice(teachers).id),
    Subject(title="Physics", teacher_id=random.choice(teachers).id),
    Subject(title="Chemistry", teacher_id=random.choice(teachers).id),
    Subject(title="Biology", teacher_id=random.choice(teachers).id),
    Subject(title="History", teacher_id=random.choice(teachers).id),
    Subject(title="Literature", teacher_id=random.choice(teachers).id),
]
db.add_all(subjects)
db.commit()  

# Створення студентів
students = [
    Student(full_name=fake.name(), group=random.choice(groups)) for _ in range(40)
]
db.add_all(students)
db.commit()  

# Створення оцінок
current_date = date.today()

for student in students:
    for _ in range(random.randint(15, 20)):
        subject = random.choice(subjects)  # Випадковий предмет
        random_days = random.randint(0, 365)
        grade_date = current_date - timedelta(days=random_days)

        grade = Grade(
            grade=random.randint(60, 100),
            student_id=student.id,
            subject_id=subject.id,
            date=grade_date, 
        )
        db.add(grade)

db.commit()  
db.close()
