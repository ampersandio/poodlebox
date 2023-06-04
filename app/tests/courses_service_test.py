import unittest
from unittest.mock import Mock
from api.services import courses
from api.data.models import Student

mock_db=Mock()
courses.database=mock_db