from api.services.authorization import create_access_token
from api.data.models import Student, Course, TeacherShow, TeacherRegistration, StudentRegistration, User

from config import settings
from mailjet_rest import Client

mailjet = Client(auth=(settings.api_key, settings.api_secret), version='v3.1')


def generate_message(from_email,from_name,to_email,to_name,subject,text_part,html_part):
    message = {'Messages': [
                    {
                            "From": {
                                    "Email": from_email,
                                    "Name": from_name
                            },
                            "To": [
                                    {
                                            "Email": to_email,
                                            "Name": to_name
                                    }
                            ],
                            "Subject": subject,
                            "TextPart": text_part,
                            "HTMLPart": html_part
                    }
                ]}
    
    return message


def generate_template(template_path,replacements):
    with open(template_path, 'r') as template:   
        html_template = template.read()

    ready_template = html_template

    for key,value in replacements.items():
        ready_template = ready_template.replace(key, str(value))

    return ready_template


def user_registration(information:StudentRegistration, host:str):

    token = create_access_token({"sub":information.email})

    replacements = {
        '{student_first_name}':str(information.first_name),
        '{student_last_name}':information.last_name,
        '{student_email}':information.email,
        '{approval_link}':f"{host}/api/authorization/token/{token}/"
    }

    html_template = generate_template("api/utils/mail_templates/user_registration.html", replacements)

    message = generate_message(
        from_email="anedelev@gmail.com",
        from_name="Poodlebox Admin",
        to_email=information.email,
        to_name=information.first_name + " " + information.last_name,
        subject="Poodlebox Mail Verification",
        text_part="Dear PoodleBox User",
        html_part=html_template
    )

    result = mailjet.send.create(data=message)

    print(result.status_code)
    print(result.json())


def enrollment_mail(student:Student, course:Course, teacher:TeacherShow):

    replacements = {
        '{student_first_name}': student.first_name,
        '{student_last_name}': student.last_name,
        '{course_title}': course.title,
    }

    html_template = generate_template("api/utils/mail_templates/enrollment_notification.html", replacements)

    message = generate_message(
        from_email="anedelev@gmail.com",
        from_name="Poodlebox Admin",
        to_email=teacher.email,
        to_name=teacher.first_name + " " + teacher.last_name,
        subject="New Student Enrollment in your course {course.title}",
        text_part="Greetings",
        html_part=html_template
    )

    result = mailjet.send.create(data=message)

    print(result.status_code)
    print(result.json())


def teacher_registration(information:TeacherRegistration):

    replacements = {
    '{teacher_first_name}': information.first_name,
    '{teacher_last_name}': information.last_name,
    '{teacher_email}': information.email
    }

    html_template = generate_template("api/utils/mail_templates/teacher_registration.html", replacements)

    message = generate_message(
        from_email="anedelev@gmail.com",
        from_name="Poodlebox Admin",
        to_email="anedelev@gmail.com",
        to_name=information.first_name + " " + information.last_name,
        subject="New Teacher Registered At Poodlebox",
        text_part="Greetings",
        html_part=html_template
    )

    result = mailjet.send.create(data=message)

    print(result.status_code)
    print(result.json())


def teacher_approval(teacher:TeacherShow):

    replacements = {
    '{teacher_first_name}': teacher.first_name,
    '{teacher_last_name}': teacher.last_name,
    '{teacher_email}': teacher.email
    }

    html_template = generate_template("api/utils/mail_templates/teacher_approved.html", replacements)

    message = generate_message(
        from_email="anedelev@gmail.com",
        from_name="Poodlebox Admin",
        to_email=teacher.email,
        to_name=teacher.first_name + " " + teacher.last_name,
        subject="Your Registration At Poodblebox Was Approved",
        text_part="Greetings",
        html_part=html_template
    )

    result = mailjet.send.create(data=message)

    print(result.status_code)
    print(result.json())

def course_deactivated(student:User, course_title:str):
    replacements = {
    '{student_first_name}':student.first_name,
    '{student_last_name}':student.last_name,
    '{student_email}':student.email,
    '{course_title}':course_title
    }

    html_template = generate_template("api/utils/mail_templates/course_status", replacements)

    message = generate_message(
        from_email="anedelev@gmail.com",
        from_name="Poodlebox Admin",
        to_email=student.email,
        to_name=student.first_name + " " + student.last_name,
        subject="Course you've been enrolled in, is now Inactive",
        text_part="Greetings",
        html_part=html_template
    )

    result = mailjet.send.create(data=message)

    print(result.status_code)
    print(result.json())
