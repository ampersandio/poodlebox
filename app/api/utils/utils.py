from api.services.authorization import create_access_token
from api.data.models import Student, Course, TeacherShow

def generate_html(email,host):
    token = create_access_token({"sub":email})
    message = {'Messages': [
                    {
                            "From": {
                                    "Email": "anedelev@gmail.com",
                                    "Name": "Verify Your Email"
                            },
                            "To": [
                                    {
                                            "Email": email,
                                            "Name": "passenger 1"
                                    }
                            ],
                            "Subject": "Poodlebox Mail Verification",
                            "TextPart": "Dear PoodleBox User",
                            "HTMLPart": f"<h3>Welcome to PoodleBox please click the link to verify your account <a href=\"{host}/api/authorization/token/{token}/\">Mailjet</a>!</h3><br />May the poodlebox force be with you!"
                    }
                ]}
    
    return message


def send_enrollment_mail(student:Student, course:Course, teacher:TeacherShow):

    with open("/Users/alexandernedelev/Desktop/Telerik_A45/poodlebox/app/assets/mail_templates/enrollment_notification.html.html", 'r') as template:
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
                            "Subject": "New Enrollment",
                            "TextPart": "Greetings",
                            "HTMLPart": ready_template
                    }
                ]}
    
    return message

