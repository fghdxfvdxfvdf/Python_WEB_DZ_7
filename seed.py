import logging
from datetime import date, datetime, timedelta
from random import choice, randint

import faker
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.db import session
from src.models import Discipline, Grade, Group, Student, Teacher

faker = faker.Faker()

disciplines = [
    "Вища математика",
    "Історія",
    "Лінійна алгебра",
    "Креслення",
    "Теорія ймовірності",
    "Історія України",
    "Англійська мова",
    "Програмування",
    "Фізика",
    "Хімія",
]
groups = ["Є331", "ТПК-155", "ЄС-97л", "КН-51", "ПЦБ-13з"]
NUMBER_STUDENTS = 50
NUMBER_TEACHERS = 5
STUDENT_FROM_ONE_DAY = 5


def date_range(start: date, end: date):
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result


def fill_data():
    def seed_teachers():
        """Seed teachers data into the database."""
        for _ in range(NUMBER_TEACHERS):
            teacher = Teacher(fullname=faker.name())
            session.add(teacher)
        session.commit()

    def seed_disciplines():
        """Seed disciplines data into the database."""
        teacher_ids = session.scalars(select(Teacher.id)).all()
        for discipline in disciplines:
            session.add(Discipline(name=discipline, teacher_id=choice(teacher_ids)))
        session.commit()

    def seed_groups():
        """Seed groups data into the database."""
        for group in groups:
            session.add(Group(name=group))
        session.commit()

    def seed_students():
        """Seed students data into the database."""
        group_ids = session.scalars(select(Group.id)).all()

        for _ in range(NUMBER_STUDENTS):
            student = Student(fullname=faker.name(), group_id=choice(group_ids))
            session.add(student)
        session.commit()

    def seed_grades():
        """Seed grades data into the database."""
        start_date = datetime.strptime("2020-09-01", "%Y-%m-%d")
        end_date = datetime.strptime("2021-05-25", "%Y-%m-%d")
        d_range = date_range(start=start_date, end=end_date)

        discipline_ids = session.scalars(select(Discipline.id)).all()
        student_ids = session.scalars(select(Student.id)).all()

        for d in d_range:
            random_id_discipline = choice(discipline_ids)
            random_id_student = [
                choice(student_ids) for _ in range(STUDENT_FROM_ONE_DAY)
            ]

            for student_id in random_id_student:
                grade = Grade(
                    grade=randint(1, 12),
                    date_of=d,
                    student_id=student_id,
                    discipline_id=random_id_discipline,
                )
                session.add(grade)
        session.commit()

    seed_teachers()
    seed_disciplines()
    seed_groups()
    seed_groups()
    seed_students()
    seed_grades()


if __name__ == "__main__":
    try:
        fill_data()

    except SQLAlchemyError as e:
        # logging.error(f"Error: {e}")
        logging.error("Error: %s", e)
        session.rollback()
    finally:
        session.close()
