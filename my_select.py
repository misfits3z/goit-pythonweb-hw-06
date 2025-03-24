from database import SessionLocal
from models import Student, Grade, Group, Teacher, Subject
from sqlalchemy.orm import Session
from sqlalchemy import func

db = SessionLocal()


# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів
def select_top_students():
    top_students = (
        db.query(Student.full_name, func.round(func.avg(Grade.grade), 0).label("avg_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )
    return top_students


# 2. Знайти студента із найвищим середнім балом з певного предмета
def top_student_for_subject(db: Session, subject_id: int):
    top_student = (
        db.query(Student.full_name, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .join(Subject)
        .filter(Subject.id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()  
    )
    return top_student


# 3. Знайти середній бал у групах з певного предмета
def average_grade_in_group_for_subject(db: Session, subject_id: int):
    average_grades = (
        db.query(Group.name, func.avg(Grade.grade).label("avg_grade"))
        .select_from(Group)
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.id == subject_id)
        .group_by(Group.id)
        .all()
    )
    return average_grades


# 4. Знайти середній бал на потоці (по всій таблиці оцінок)
def average_grade_for_all(db: Session):
    average_grade = db.query(func.avg(Grade.grade).label("avg_grade")).scalar()
    return average_grade


# 5. Знайти які курси читає певний викладач
def courses_by_teacher(db: Session, teacher_id: int):
    courses = (
        db.query(Subject.title).join(Teacher).filter(Teacher.id == teacher_id).all()
    )
    return courses


# 6. Знайти список студентів у певній групі
def students_in_group(db: Session, group_id: int):
    students = db.query(Student.full_name).join(Group).filter(Group.id == group_id).all()
    return students


# 7. Знайти оцінки студентів у окремій групі з певного предмета
def grades_for_group_subject(db: Session, group_id: int, subject_id: int):
    grades = (
        db.query(Student.full_name, Grade.grade)
        .join(Group)
        .join(Grade)
        .join(Subject)
        .filter(Group.id == group_id)
        .filter(Subject.id == subject_id)
        .all()
    )
    return grades


# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів
def average_grade_by_teacher(db: Session, teacher_id: int):
    avg_grades = (
        db.query(func.avg(Grade.grade).label("avg_grade"))
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.id == teacher_id)
        .scalar()
    )
    return avg_grades


# 9. Знайти список курсів, які відвідує певний студент
def courses_by_student(db: Session, student_id: int):
    courses = (
        db.query(Subject.title).join(Grade).filter(Grade.student_id == student_id).all()
    )
    return courses


# 10. Список курсів, які певному студенту читає певний викладач
def courses_by_student_teacher(db: Session, student_id: int, teacher_id: int):
    courses = (
        db.query(Subject.title)
        .join(Grade)
        .join(Teacher)
        .filter(Grade.student_id == student_id)
        .filter(Teacher.id == teacher_id)
        .all()
    )
    return courses


# Приклад використання:
if __name__ == "__main__":
    # 1. Отримати 5 студентів із найбільшим середнім балом
    top_students = select_top_students()
    print("Top students:", top_students)

    # 2. Студент із найвищим середнім балом з випадкового предмета
    subject = (
        db.query(Subject).order_by(func.random()).first()
    )  # Вибір випадкового предмета
    if subject is not None:
        top_student = top_student_for_subject(db, subject_id=subject.id)
        print(f"Top student for subject {subject.title}: {top_student}")
    else:
        print("No subjects found.")

    # 3. Середній бал у групах з випадкового предмета
    subject = (
        db.query(Subject).order_by(func.random()).first()
    )  # Вибір випадкового предмета
    if subject is not None:
        average_grades = average_grade_in_group_for_subject(db, subject_id=subject.id)
        print(f"Average grades in groups for subject {subject.title}: {average_grades}")
    else:
        print("No subjects found.")

    # 4. Середній бал на потоці
    avg_grade = average_grade_for_all(db)
    print("Average grade for all students:", avg_grade)

    # 5. Курси випадкового викладача
    teacher = (
        db.query(Teacher).order_by(func.random()).first()
    )  # Вибір випадкового викладача
    if teacher is not None:
        courses = courses_by_teacher(db, teacher_id=teacher.id)
        print(f"Courses by teacher {teacher.full_name}: {courses}")
    else:
        print("No teachers found.")

    # 6. Список студентів у випадковій групі
    group = db.query(Group).order_by(func.random()).first()  # Вибір випадкової групи
    if group is not None:
        students = students_in_group(db, group_id=group.id)
        print(f"Students in group {group.name}: {students}")
    else:
        print("No groups found.")

    # 7. Оцінки студентів у випадковій групі з випадкового предмета
    group = db.query(Group).order_by(func.random()).first()  # Вибір випадкової групи
    subject = (
        db.query(Subject).order_by(func.random()).first()
    )  # Вибір випадкового предмета
    if group is not None and subject is not None:
        grades = grades_for_group_subject(db, group_id=group.id, subject_id=subject.id)
        print(f"Grades for group {group.name} and subject {subject.title}: {grades}")
    else:
        print("No groups or subjects found.")

    # 8. Середній бал, який ставить випадковий викладач
    teacher = (
        db.query(Teacher).order_by(func.random()).first()
    )  # Вибір випадкового викладача
    if teacher is not None:
        avg_teacher_grade = average_grade_by_teacher(db, teacher_id=teacher.id)
        print(f"Average grade by teacher {teacher.full_name}: {avg_teacher_grade}")
    else:
        print("No teachers found.")

    # 9. Курси, які відвідує випадковий студент
    student = (
        db.query(Student).order_by(func.random()).first()
    )  # Вибір випадкового студента
    if student is not None:
        student_courses = courses_by_student(db, student_id=student.id)
        print(f"Courses by student {student.full_name}: {student_courses}")
    else:
        print("No students found.")

    # 10. Курси, які студенту читає випадковий викладач
    student = (
        db.query(Student).order_by(func.random()).first()
    )  # Вибір випадкового студента
    teacher = (
        db.query(Teacher).order_by(func.random()).first()
    )  # Вибір випадкового викладача
    if student is not None and teacher is not None:
        student_teacher_courses = courses_by_student_teacher(db, student_id=student.id, teacher_id=teacher.id)
        print(
            f"Courses by student {student.full_name} and teacher {teacher.full_name}: {student_teacher_courses}"
        )
    else:
        print("No students or teachers found.")

    db.close()
