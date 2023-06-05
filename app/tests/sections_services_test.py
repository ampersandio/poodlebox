import unittest
from unittest.mock import Mock, patch
from api.services.courses import get_section_by_id
from api.data.models import Section, Content

class SectionServiceTestCase(unittest.TestCase):

    def test_get_section_by_id_existing_section_and_content(self):
        with patch('api.services.courses.read_query') as mock_read_query:
            mock_read_query.side_effect = [
                [(1, 'Section Title')],
                [(1, 'Content 1', 'Description 1', 'Type 1', 'Link 1')]
            ]

            result = get_section_by_id(1)

            expected_section = Section(id=1,title='Section Title',content=[Content(id=1, title='Content 1', description='Description 1', content_type='Type 1', link='Link 1')])

            self.assertEqual(result, expected_section)
            self.assertIsInstance(expected_section, Section)
            self.assertIsInstance(expected_section.content[0], Content)

    def test_get_section_by_id_existing_section_without_content(self):
        with patch('api.services.courses.read_query') as mock_read_query:
            mock_read_query.side_effect = [
                [(1, 'Section Title')],
                []
            ]

            result = get_section_by_id(1)

            expected_section = Section(id=1,title='Section Title',content=[])

            self.assertEqual(result, expected_section)
            self.assertIsInstance(expected_section, Section)
            self.assertEqual(expected_section.content, [])

    def test_get_section_by_id_non_existing_section(self):
        with patch('api.services.courses.read_query') as mock_read_query:
            mock_read_query.return_value = []

            result = get_section_by_id(1)

            self.assertIsNone(result)