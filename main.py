from sqlalchemy import desc, func

from src.db import session
from src.models import Discipline, Grade, Group, Student, Teacher


def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    result = (
        session.query(
            Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )
    return result


def select_2(discipline_id):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    result = (
        session.query(
            Discipline.name,
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .filter(Discipline.id == discipline_id)
        .group_by(Student.id, Discipline.name)
        .order_by(desc("avg_grade"))
        .limit(1)
        .all()
    )
    return result


def select_3(discipline_id):
    """Знайти середній бал у групах для певного предмета."""
    result = (
        session.query(
            Discipline.name,
            Group.name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .join(Discipline)
        .join(Student)
        .join(Group)
        .filter(Discipline.id == discipline_id)
        .group_by(Group.id, Discipline.name)
        .order_by(desc("avg_grade"))
        .all()
    )
    return result


def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    result = session.query(func.round(func.avg(Grade.grade), 2).label("avg")).first()
    return result


def select_5(teacher_id):
    """Знайти курси, які читає певний викладач."""
    result = (
        session.query(Discipline.name)
        .join(Teacher)
        .filter(Teacher.id == teacher_id)
        .all()
    )
    return result


def select_6(group_id):
    """Знайти список студентів у певній групі."""
    result = (
        session.query(Student.fullname).join(Group).filter(Group.id == group_id).all()
    )
    return result


def select_7(group_id, discipline_id):
    """Знайти оцінки студентів у конкретній групі з певного предмета."""
    result = (
        session.query(Student.fullname, Grade.grade)
        .join(Group)
        .join(Grade)
        .join(Discipline)
        .filter(Group.id == group_id, Discipline.id == discipline_id)
        .all()
    )
    return result


def select_8(teacher_id):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    result = (
        session.query(func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .join(Discipline)
        .join(Teacher)
        .filter(Teacher.id == teacher_id)
        .first()
    )
    return result


def select_9(student_id):
    """Знайти список курсів, які відвідує певний студент."""
    result = (
        session.query(Discipline.name)
        .join(Grade)
        .join(Student)
        .filter(Student.id == student_id)
        .distinct()
        .group_by(Student.id, Discipline.name)
        .all()
    )
    return result


def select_10(student_id, teacher_id):
    """Знайти список курсів, які певний студент відвідує від певного викладача."""
    result = (
        session.query(Discipline.name)
        .join(Grade)
        .join(Student)
        .join(Teacher)
        .filter(Student.id == student_id, Teacher.id == teacher_id)
        .distinct()
        .all()
    )
    return result


if __name__ == "__main__":
    print('Знайти 5 студентів із найбільшим середнім балом з усіх предметів:', select_1())
    print('____________________________________________')
    
    print('Знайти студента із найвищим середнім балом з певного предмета:', select_2(discipline_id=2))
    print('____________________________________________')
    
    print('Знайти середній бал у групах для певного предмета:', select_3(discipline_id=2))
    print('____________________________________________')

    print('Знайти середній бал на потоці (по всій таблиці оцінок):', select_4())
    print('____________________________________________')
    
    print('Знайти курси, які читає певний викладач:', select_5(teacher_id=3))
    print('____________________________________________')
    
    print('Знайти список студентів у певній групі:', select_6(group_id=2))
    print('____________________________________________')
    
    print('Знайти оцінки студентів у конкретній групі з певного предмета:', select_7(group_id=2, discipline_id=3))
    print('____________________________________________')
   
    print('Знайти середній бал, який ставить певний викладач зі своїх предметів:', select_8(teacher_id=3))
    print('____________________________________________')
    
    print('Знайти список курсів, які відвідує певний студент:', select_9(student_id=1))
    print('____________________________________________')
    
    print('Знайти список курсів, які певний студент відвідує від певного викладача:', select_10(student_id=1, teacher_id=3))
