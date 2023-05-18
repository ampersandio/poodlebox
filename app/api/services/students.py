from data.database import read_query
def get_students_courses(student_id):
    data_course=read_query("select c.id,c.title,c.description,c.objectives,c.premium,ifnull(round(sum(r.rating)/count(r.id),2),0) as rating,c.price,group_concat(distinct t.name) as tags,u.id,u.first_name,u.last_name,u.phone_number,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id where c.premium=0 group by c.id,c.title,c.description,c.objectives,c.price,u.first_name,u.last_name,u.phone_number,u.linked_in_profile,c.premium,u.id",(course_id,))
    data_sections=read_query("select id,title from sections where courses_id=?",(course_id,))
    list_sections=[Section.read_from_query_result(*row,content=None) for row in data_sections]
    for x in list_sections:
        data_content=read_query("select c.id,c.title,c.description,c.content_types_id from content c join sections s on s.id=c.sections_id where s.title=?",(x.title,))
        list_content=[Content.read_from_query_result(*row) for row in data_content]
        x.content=list_content
    data_course=read_query("select c.id,c.title,c.description,c.objectives,c.premium,round(sum(r.rating)/count(r.id),2) as rating,c.price,group_concat(distinct t.name) as tags,u.id,u.first_name,u.last_name,u.phone_number,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id where c.id=? group by c.id",(course_id,))
    if data_course==[]:
        return "Not found"
    owner=(TeacherShow.read_from_query_result(*data_course[0][8:]))
    course=(CourseShowId.read_from_query_result(*data_course[0][:8],teacher=owner,sections=list_sections))

    return course   
