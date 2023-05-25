from api.services.authorization import create_access_token
from api.data.models import Student, Course, TeacherShow, TeacherRegistration, StudentRegistration


def user_registration(information:StudentRegistration, host:str):

    token = create_access_token({"sub":information.email})
    print(token)

    with open("api/utils/mail_templates/student_registration.html", 'r') as template:   
        html_template = template.read()

    ready_template = html_template.replace ('{student_first_name}', str(information.first_name ))
    ready_template = ready_template.replace('{student_last_name}', str(information.last_name))
    ready_template = ready_template.replace('{student_email}', str(information.email))
    ready_template = ready_template.replace('{approval_link}', str(f"{host}/api/authorization/token/{token}/"))

    message = {'Messages': [
                    {
                            "From": {
                                    "Email": "anedelev@gmail.com",
                                    "Name": "Verify Your Email"
                            },
                            "To": [
                                    {
                                            "Email": information.email,
                                            "Name": "passenger 1"
                                    }
                            ],
                            "Subject": "Poodlebox Mail Verification",
                            "TextPart": "Dear PoodleBox User",
                            "HTMLPart": ready_template
                    }
                ]}
    
    return message


def enrollment_mail(student:Student, course:Course, teacher:TeacherShow):

    with open("api/utils/mail_templates/enrollment_notification.html", 'r') as template:   
        html_template = template.read()

    ready_template = html_template.replace ('{student_first_name}', str(student.first_name ))
    ready_template = ready_template.replace('{student_last_name}', str(student.last_name))
    ready_template = ready_template.replace('{course_title}', str(course.title))

    message = {'Messages': [
                    {
                            "From": {
                                    "Email": "anedelev@gmail.com",
                                    "Name": "Student Enrolled in Your Class"
                            },
                            "To": [
                                    {
                                            "Email": f"{teacher.email}",
                                            "Name": f" {teacher .first_name} {teacher. last_name}"
                                    }
                            ],
                            f"Subject": "New Student Enrollment in your course {course.title}",
                            "TextPart": "Greetings",
                            "HTMLPart": ready_template
                    }
                ]}
    
    return message


def teacher_registration(information:TeacherRegistration):

    with open("api/utils/mail_templates/teacher_registration.html", 'r') as template:   
        html_template = template.read()

    ready_template = html_template.replace ('{teacher_first_name}', str(information.first_name ))
    ready_template = ready_template.replace('{teacher_last_name}', str(information.last_name))
    ready_template = ready_template.replace('{teacher_email}', str(information.email))

    message = {'Messages': [
                    {
                            "From": {
                                    "Email": "anedelev@gmail.com",
                                    "Name": "Teacher Registered"
                            },
                            "To": [
                                    {
                                            "Email": "anedelev@gmail.com",
                                            "Name": f" {information.first_name} {information.last_name}"
                                    }
                            ],
                            "Subject": "New Teacher Registered At Poodlebox",
                            "TextPart": "Greetings",
                            "HTMLPart": ready_template
                    }
                ]}
    
    return message


def teacher_approval(teacher:TeacherShow):
    print(teacher)
    with open("api/utils/mail_templates/teacher_approved.html", 'r') as template:   
        html_template = template.read()

    ready_template = html_template.replace ('{teacher_first_name}', str(teacher.first_name ))
    ready_template = ready_template.replace('{teacher_last_name}', str(teacher.last_name))
    ready_template = ready_template.replace('{teacher_email}', str(teacher.email))

    message = {'Messages': [
                    {
                            "From": {
                                    "Email": "anedelev@gmail.com",
                                    "Name": "Teacher Registered"
                            },
                            "To": [
                                    {
                                            "Email": f"{teacher.email}",
                                            "Name": f"{teacher.first_name} {teacher.last_name}"
                                    }
                            ],
                            "Subject": "Your Registration At Poodblebox Was Approved",
                            "TextPart": "Greetings",
                            "HTMLPart": ready_template
                    }
                ]}
    
    return message

