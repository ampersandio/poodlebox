from data.database import read_query
from data.models import TeacherShow, CourseShow, Section,Content, CourseShowId
def get_courses_anonymous_and_teacher():
    data=read_query("select c.id,c.title,c.description,c.objectives,c.premium,ifnull(round(sum(r.rating)/count(r.id),2),0) as rating,c.price,group_concat(distinct t.name) as tags,u.id,u.first_name,u.last_name,u.phone_number,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id group by c.id,c.title,c.description,c.objectives,c.price,u.first_name,u.last_name,u.phone_number,u.linked_in_profile,c.premium,u.id")
    list_courses=[]
    for x in range(len(data)):
        owner=(TeacherShow.read_from_query_result(*data[x][8:]))
        course=(CourseShow.read_from_query_result(*data[x][:8],teacher=owner))
        list_courses.append(course)
    return list_courses
    
def get_courses_student(student_id):
    data_courses=read_query("select c.id from courses c join users_has_courses uc on uc.courses_id=c.id where uc.users_id=? and (uc.subscriptions_id=? or uc.subscriptions_id=?)",(student_id,2,3))
    if data_courses==[]:
        return get_courses_anonymous_and_teacher()
    data=read_query("select c.id,c.title,c.description,c.objectives,c.premium,ifnull(round(sum(r.rating)/count(r.id),2),0) as rating,c.price,group_concat(distinct t.name) as tags,u.id,u.first_name,u.last_name,u.phone_number,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id where t.name in (select t.name from tags t join interests i on t.id=i.tags_id where i.users_id=?) and c.id not in (select c.id from courses c left join users_has_courses uc on c.id=uc.courses_id where uc.users_id=?) group by c.id,c.title,c.description,c.objectives,c.price,u.first_name,u.last_name,u.phone_number,u.linked_in_profile,u.id,c.premium  union select c.id,c.title,c.description,c.objectives,c.premium,ifnull(round(sum(r.rating)/count(r.id),2),0) as rating,c.price,group_concat(distinct t.name) as tags,u.id,u.first_name,u.last_name,u.phone_number,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id left join users_has_courses uc on uc.courses_id=c.id where t.name not in (select t.name from tags t join interests i on t.id=i.tags_id where i.users_id=?) and c.id not in (select c.id from courses c join users_has_courses uc on c.id=uc.courses_id where uc.users_id=?) group by c.id,c.title,c.description,c.objectives,c.price,u.first_name,u.last_name,u.phone_number,u.linked_in_profile,c.id,c.premium,u.id union select c.id,c.title,c.description,c.objectives,c.premium,ifnull(round(sum(r.rating)/count(r.id),2),0)  as rating,c.price,group_concat(distinct t.name) as tags,u.id,u.first_name,u.last_name,u.phone_number,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id where c.id in (select c.id from courses c join users_has_courses uc on c.id=uc.courses_id where uc.users_id=?) group by c.id,c.title,c.description,c.objectives,c.price,u.first_name,u.last_name,u.phone_number,u.linked_in_profile,u.id,c.premium",(student_id,student_id,student_id,student_id))
    list_courses=[]
    for x in range(len(data)):
        owner=(TeacherShow.read_from_query_result(*data[x][8:]))
        course=(CourseShow.read_from_query_result(*data[x][:8],teacher=owner))
        list_courses.append(course)
    return list_courses

def get_course_by_id(course_id):
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




