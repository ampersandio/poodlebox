import unittest
from unittest.mock import Mock, patch
from api.services.courses import get_section_by_id, get_course_sections,n_visited_sections
from api.data.models import Section, Content

class SectionServiceTestCase(unittest.TestCase):

    @patch("api.services.courses.read_query")
    def test_get_section_by_id_existing_section_and_content(self,mock_read_query):
            mock_read_query.side_effect = [
                [(1, 'Section Title')],
                [(1, 'Content 1', 'Description 1', 'Type 1', 'Link 1')]
            ]

            result = get_section_by_id(1)

            expected_section = Section(id=1,title='Section Title',content=[Content(id=1, title='Content 1', description='Description 1', content_type='Type 1', link='Link 1')])

            self.assertEqual(result, expected_section)
            self.assertIsInstance(expected_section, Section)
            self.assertIsInstance(expected_section.content[0], Content)


    @patch("api.services.courses.read_query")
    def test_get_section_by_id_existing_section_without_content(self, mock_read_query):
            mock_read_query.side_effect = [
                [(1, 'Section Title')],
                []
            ]

            result = get_section_by_id(1)

            expected_section = Section(id=1,title='Section Title',content=[])

            self.assertEqual(result, expected_section)
            self.assertIsInstance(expected_section, Section)
            self.assertEqual(expected_section.content, [])

    @patch("api.services.courses.read_query")
    def test_get_section_by_id_non_existing_section(self, mock_read_query):
            mock_read_query.return_value = []

            result = get_section_by_id(1)

            self.assertIsNone(result)

    @patch("api.services.courses.read_query")
    def test_get_course_sections(self,mock_read_query):
            mock_read_query.side_effect = [
                [(1, 'Section 1'), (2, 'Section 2')],
                [(1, 'Content 1', 'Description 1', 'Type 1', 'Link 1')],
                [(2, 'Content 2', 'Description 2', 'Type 2', 'Link 2')]
            ]

            result = get_course_sections(1)

            expected_section_1 = Section(id=1, title='Section 1', content=[Content(id=1, title='Content 1', description='Description 1', content_type='Type 1', link='Link 1')])
            expected_section_2 = Section(id=2, title='Section 2', content=[Content(id=2, title='Content 2', description='Description 2', content_type='Type 2', link='Link 2')])
            expected_sections = [expected_section_1, expected_section_2]

            self.assertEqual(result, expected_sections)

    @patch("api.services.courses.read_query")
    def test_get_course_sections_empty(self,mock_read_query):
            mock_read_query.return_value = []

            result = get_course_sections(1)

            self.assertEqual(result, [])

    @patch("api.services.courses.read_query")
    def test_get_course_sections_single_section_no_content(self, mock_read_query):

            mock_read_query.side_effect = [
                [(1, 'Section 1')],
                []  
            ]

            result = get_course_sections(1)

            expected_section = Section(id=1, title='Section 1', content=[])

            self.assertEqual(result, [expected_section])


    @patch("api.services.courses.read_query")
    def test_get_course_sections_multiple_sections_no_content(self, mock_read_query):
            mock_read_query.side_effect = [
                [(1, 'Section 1'), (2, 'Section 2')],
                [], 
                []   
            ]

            result = get_course_sections(1)

            expected_section_1 = Section(id=1, title='Section 1', content=[])
            expected_section_2 = Section(id=2, title='Section 2', content=[])

            self.assertEqual(result, [expected_section_1, expected_section_2])

    @patch("api.services.courses.read_query")
    def test_n_visited_sections(self, mock_read_query):

        mock_read_query.return_value = [[3]] 

        expected_result = 3

        result = n_visited_sections(1, 6)

        self.assertEqual(result, expected_result)
