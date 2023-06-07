import unittest
from unittest.mock import Mock, patch
from api.services.courses import get_section_by_id,delete_section, get_course_students,add_content,get_most_popular, get_course_sections,n_visited_sections,add_course_photo,create_section, insert_section, get_content_type_id, insert_content, insert_content_type,get_content_by_id, update_section
from api.data.models import Section, Content, SectionCreate, ContentCreate, Course, User

EXPECTED_SECTION_1 = Section(id=1,title='Section 1',content=[Content(id=1, title='Content 1', description='Description 1', content_type='Type 1', link='Link 1')])
EXPECTED_SECTION_2 = Section(id=2, title='Section 2', content=[Content(id=2, title='Content 2', description='Description 2', content_type='Type 2', link='Link 2')])
EXPECTED_SECTION_NO_CONTENT_1 = Section(id=1, title='Section 1', content=[])
EXPECTED_SECTION_NO_CONTENT_2 = Section(id=2, title='Section 2', content=[])
COURSE_1 = Course(title='Title 1', description='Description 1', objectives='Objectives 1', premium=False, price=None, course_picture='Image 1', id=6, active=True, owner=1)

class SectionServiceTestCase(unittest.TestCase):

	@patch("api.services.courses.read_query")
	def test_get_section_by_id_existing_section_and_content(self,mock_read_query):
		mock_read_query.side_effect = [
			[(1, 'Section 1')],
			[(1, 'Content 1', 'Description 1', 'Type 1', 'Link 1')]
		]

		result = get_section_by_id(1)

		self.assertEqual(result, EXPECTED_SECTION_1)
		self.assertIsInstance(EXPECTED_SECTION_1, Section)
		self.assertIsInstance(EXPECTED_SECTION_1.content[0], Content)


	@patch("api.services.courses.read_query")
	def test_get_section_by_id_existing_section_without_content(self, mock_read_query):
		mock_read_query.side_effect = [
			[(1, 'Section 1')],
			[]
		]

		result = get_section_by_id(1)

		self.assertEqual(result, EXPECTED_SECTION_NO_CONTENT_1)
		self.assertIsInstance(EXPECTED_SECTION_NO_CONTENT_1, Section)
		self.assertEqual(EXPECTED_SECTION_NO_CONTENT_1.content, [])


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

		expected_sections = [EXPECTED_SECTION_1, EXPECTED_SECTION_2]

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


		self.assertEqual(result, [EXPECTED_SECTION_NO_CONTENT_1])


	@patch("api.services.courses.read_query")
	def test_get_course_sections_multiple_sections_no_content(self, mock_read_query):
		mock_read_query.side_effect = [
			[(1, 'Section 1'), (2, 'Section 2')],
			[], 
			[]   
		]

		result = get_course_sections(1)

		self.assertEqual(result, [EXPECTED_SECTION_NO_CONTENT_1, EXPECTED_SECTION_NO_CONTENT_2])


	@patch("api.services.courses.read_query")
	def test_n_visited_sections(self, mock_read_query):

		expected_result = 3

		mock_read_query.return_value = [[3]]

		result = n_visited_sections(1, 6)

		mock_read_query.assert_called_once_with(
            "select count(*) from users_has_sections as us join sections as s on us.sections_id = s.id where us.users_id = ? and s.courses_id = ?;",
            (1, 6),
        )

		self.assertEqual(result, expected_result)


	@patch("api.services.courses.get_course_by_id")
	@patch("api.services.courses.insert_query")
	def test_add_course_photo_existing_course(self, mock_insert_query, mock_get_course_by_id):

		mock_get_course_by_id.return_value = {'id': 1, 'course_picture': None}

		add_course_photo('photo.jpg', 1)

		mock_insert_query.assert_called_once_with("update courses set course_picture = ? where id = ?", ('photo.jpg', 1,))


	@patch("api.services.courses.get_course_by_id")
	@patch("api.services.courses.insert_query")
	def test_add_course_photo_non_existing_course(self, mock_insert_query, mock_get_course_by_id):

		mock_get_course_by_id.return_value = None

		result = add_course_photo('photo.jpg', 1)

		mock_insert_query.assert_not_called()

		self.assertIsNone(result)


	@patch("api.services.courses.insert_section")
	@patch("api.services.courses.get_content_type_id")
	@patch("api.services.courses.insert_content")
	@patch("api.services.courses.get_section_by_id")
	def test_create_section_with_content(self, mock_get_section_by_id, mock_insert_content, mock_get_content_type_id, mock_insert_section):
		course_id = 1
		section_data = SectionCreate(title='Section 1', content=[ContentCreate(title='Content 1', description='Description 1', content_type='Type 1', link='Link 1')])
		last_section_id = 10
		content_type_id = 5

		mock_insert_section.return_value = last_section_id
		mock_get_content_type_id.return_value = content_type_id

		mock_get_section_by_id.return_value = EXPECTED_SECTION_1

		result = create_section(course_id, section_data)

		mock_insert_section.assert_called_once_with(section_data.title, course_id)
		mock_get_content_type_id.assert_called_once_with(section_data.content[0].content_type)
		mock_insert_content.assert_called_once_with(section_data.content[0].title, section_data.content[0].description, content_type_id, last_section_id)
		mock_get_section_by_id.assert_called_once_with(last_section_id)

		self.assertEqual(result, EXPECTED_SECTION_1)


	@patch("api.services.courses.insert_section")
	@patch("api.services.courses.get_section_by_id")
	def test_create_section_without_content(self, mock_get_section_by_id, mock_insert_section):
		course_id = 1
		section_data = SectionCreate(title='Section 1', content=None)
		last_section_id = 10

		mock_insert_section.return_value = last_section_id

		expected_section = EXPECTED_SECTION_NO_CONTENT_1
		mock_get_section_by_id.return_value = expected_section

		result = create_section(course_id, section_data)

		mock_insert_section.assert_called_once_with(section_data.title, course_id)
		mock_get_section_by_id.assert_called_once_with(last_section_id)

		self.assertEqual(result, expected_section)


	@patch("api.services.courses.insert_query")
	def test_insert_section(self, mock_insert_query):
		title = "New Section"
		course_id = 1
		expected_section_id = 10

		mock_insert_query.return_value = expected_section_id

		section_id = insert_section(title, course_id)

		mock_insert_query.assert_called_once_with(
			"INSERT INTO sections (title, courses_id) VALUES (?, ?);", (title, course_id)
		)
		self.assertEqual(section_id, expected_section_id)


	@patch("api.services.courses.read_query")
	def test_get_content_type_id_existing_content_type(self, mock_read_query):
		content_type = "Type 1"
		expected_content_type_id = 5

		mock_read_query.return_value = [(expected_content_type_id,)]

		content_type_id = get_content_type_id(content_type)

		mock_read_query.assert_called_once_with(
			"SELECT id FROM content_types WHERE type = ?;", (content_type,)
		)
		self.assertEqual(content_type_id, expected_content_type_id)


	@patch("api.services.courses.read_query")
	def test_get_content_type_id_non_existing_content_type(self, mock_read_query):
		content_type = "Type 3"

		mock_read_query.return_value = []

		content_type_id = get_content_type_id(content_type)

		mock_read_query.assert_called_once_with(
			"SELECT id FROM content_types WHERE type = ?;", (content_type,)
		)
		self.assertIsNone(content_type_id)


	@patch("api.services.courses.insert_query")
	def test_insert_content(self, mock_insert_query):
		title = "Content 1"
		description = "Description 1"
		content_type_id = 5
		section_id = 1
		link = "Dummy Link"

		insert_content(title, description, content_type_id, section_id, link)

		mock_insert_query.assert_called_once_with(
			"INSERT INTO content (title, description, content_types_id, sections_id, link) VALUES (?, ?, ?, ?, ?);",
			(title, description, content_type_id, section_id, link),
		)


	@patch("api.services.courses.insert_query")
	def test_insert_content_type(self, mock_insert_query):
		content_type = "Type 1"

		insert_content_type(content_type)

		mock_insert_query.assert_called_once_with(
			"INSERT INTO content_types (type) VALUES (?);",
			(content_type,),
		)


	@patch("api.services.courses.update_query")
	@patch("api.services.courses.get_section_by_id")
	def test_update_section(self, mock_get_section_by_id, mock_update_query):
		section_id = 1
		new_section = SectionCreate(title="Section 1")

		mock_update_query.return_value = section_id
		mock_get_section_by_id.return_value = EXPECTED_SECTION_NO_CONTENT_1

		result = update_section(section_id, new_section)

		mock_update_query.assert_called_once_with("update sections set title = ? where id = ?;",(new_section.title, section_id),)
		mock_get_section_by_id.assert_called_once_with(section_id)

		self.assertEqual(result, EXPECTED_SECTION_NO_CONTENT_1)


	@patch("api.services.courses.read_query")
	def test_get_content_by_id_existing_content(self, mock_read_query):
		content_id = 1
		mock_read_query.return_value = [(content_id, 'Sample Title', 'Sample Description', 1, "Dummy Link")]

		result = get_content_by_id(content_id)

		expected_content = Content(
			id=content_id,
			title='Sample Title',
			description='Sample Description',
			content_type=1,  # Replace 'Type 1' with the actual content type value
			link='Dummy Link'
		)

		self.assertEqual(result, [expected_content])


	@patch("api.services.courses.read_query")
	def test_get_content_by_id_no_content(self, mock_read_query):
		content_id = 1
		mock_read_query.return_value = []

		result = get_content_by_id(content_id)

		expected_content = []

		self.assertEqual(result, [])


	@patch("api.services.courses.read_query")
	@patch("api.services.courses.insert_content_type")
	@patch("api.services.courses.insert_content")
	@patch("api.services.courses.get_content_by_id")
	def test_add_content(self, mock_get_content_by_id, mock_insert_content, mock_insert_content_type, mock_read_query):

		section_id = 1
		content = ContentCreate(title='Content 1', description='Description 1', content_type='Article', link='Dummy Link')

		mock_read_query.return_value = []  
		mock_insert_content_type.return_value = 1  
		mock_insert_content.return_value = 1 
		mock_get_content_by_id.return_value = [Content( id=1, title="Content 1", description="Description 1", content_type=1)]  

		result = add_content(section_id, content)

		mock_read_query.assert_called_once_with("select id from content_types where type = ?;", ("Article",))
		mock_insert_content_type.assert_called_once_with("Article")
		mock_insert_content.assert_called_once_with("Content 1", "Description 1", 1, 1, "Dummy Link")
		self.assertEqual(result, [Content(id=1,title="Content 1",description="Description 1",content_type=1)])


	@patch("api.services.courses.read_query")
	def test_get_most_popular_with_no_role(self, mock_read_query):
		mock_read_query.return_value = [(6, 'Title 1', 'Description 1', 'Objectives 1', 0, 1, 1, None, 'Image 1')]

		result = get_most_popular()

		self.assertEqual(result, [COURSE_1])

	@patch("api.services.courses.read_query")
	def test_get_course_students(self, mock_read_query):
		mock_read_query.return_value = [(1, 'email@email.com', 'First_Name', 'Last_Name', 'Hashed_Password', 'Phone', '1776-05-18', 1, 1, 2, 'Linked_In', 0, None)]

		course_id = 1

		result = get_course_students(course_id)

		user = User(id=1, email='email@email.com', first_name='First_Name', last_name="Last_Name", hashed_password="Hashed_Password", phone_number="Phone",
	      date_of_birth='1776-05-18',verified_email=1, approved=1, role="teacher", linked_in_profile="Linked_In", disabled=0, profile_picture=None)
		
		self.assertEqual(result,[user])

	@patch("api.services.courses.get_section_by_id")
	def test_delete_section_invalid_section(self, mock_get_section_by_id):
		mock_get_section_by_id.return_value = None

		section_id = 1

		result = delete_section(section_id)

		self.assertEqual(result,None)


	@patch("api.services.courses.get_section_by_id")
	@patch("api.services.courses.update_query")
	def test_delete_section(self,mock_update_query, mock_get_section_by_id):
		mock_get_section_by_id.return_value = EXPECTED_SECTION_1
		mock_update_query.return_value = 1

		result = delete_section(1)

		mock_update_query.assert_called_once_with("delete from sections where id = ?;", (1,))