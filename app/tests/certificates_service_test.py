import unittest
from api.services import certificates
from api.data.models import Certificate

class CertificateServiceShould(unittest.TestCase):
    def test_create_certificate(self):
        db=lambda q,id:[(1,)]
        expected=None
        result=certificates.create_certificate(1,2,"2023-10-11",db)
        self.assertEqual(expected,result)
    
    def test_get_certificatesWithData(self):
        db=lambda q,id:[(1,2,2,"2023-10-11")]
        result=certificates.get_certificates(1,db)
        self.assertEqual(len(result),1)
    
    def test_get_certificatesNoData(self):
        db=lambda q,id:[]
        expected=[]
        result=certificates.get_certificates(1,db)
        self.assertEqual(expected,result)
    
    def test_get_certficateByCourseIdWithData(self):
        db=lambda q,id:[(1,2,2,"2023-10-11")]
        data=[(1,2,2,"2023-10-11")]
        expected=next((Certificate.read_from_query_result(*row) for row in data),None)
        result=certificates.get_certificate_by_course(2,2,db)
        self.assertEqual(expected,result)
    
    def test_verify_certificateTrue(self):
        db=lambda q,id:[(1,)]
        expected=True
        result=certificates.verify_certificate(2,db)
        self.assertEqual(expected,result)
        

    def test_verify_certificateFalse(self):
        db=lambda q,id:[]
        expected=False
        result=certificates.verify_certificate(2,db)
        self.assertEqual(expected,result)  