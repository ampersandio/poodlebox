from api.services.authorization import create_access_token

def generate_html(email):
    token = create_access_token(email)
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
                            "HTMLPart": f"<h3>Welcome to PoodleBox please click the link to verify your account <a href=\"http://localhost:8000/mail/{token}/\">Mailjet</a>!</h3><br />May the poodlebox force be with you!"
                    }
                ]}
    
    return message