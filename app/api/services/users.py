from api.data.database import read_query, insert_query
from api.data.models import User, StudentRegistration, TeacherRegistration


def get_user(email: str) -> User | None:
    user_data = read_query('SELECT * FROM users WHERE email=?', (email,))

    if not user_data:
        return None
    
    user = User.from_query(*user_data[0])
    return user


def register_student(student_info: StudentRegistration) -> None:
    insert_query('INSERT INTO users(email, first_name, last_name, password, date_of_birth, verified, disabled) VALUES(?,?,?,?,?,?,?);' +
                 'INSERT INTO roles(type) VALUES(?) WHERE id=(SELECT TOP 1 id FROM users)',(
        student_info.email,
        student_info.first_name,
        student_info.last_name,
        student_info.password,
        student_info.date_of_birth,
        False,
        False

        )
    )


def register_teacher(teacher_info: TeacherRegistration) -> None:
    insert_query('INSERT INTO users(email, first_name,) last_name, password, phone_number, date_of_birth, verified, role, linked_in_profile, disabled) VALUES(?,?,?,?,?,?,?,?,?,?)', (
        teacher_info.email,
        teacher_info.first_name,
        teacher_info.last_name,
        teacher_info.password,
        teacher_info.phone_number,
        teacher_info.date_of_birth,
        False,
        2,
        False
        )
    )
