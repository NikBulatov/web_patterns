from datetime import date

from nick_framework.templator import render, CreateView, ListView
from patterns.utils import Logger, Route, Debug
from patterns.mappers import MapperRegistry
from patterns.engine import Engine,BaseSerializer, UnitOfWork
from patterns.courses import EmailNotifier, SMSNotifier

engine = Engine()
logger = Logger("app")
email_notifier = EmailNotifier()
sms_notifier = SMSNotifier()
routes = {}
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@Route(routes, "/")
class IndexView:
    def __call__(self, request: dict) -> tuple[str, str]:
        return "200 OK", render("index.html.jinja", objects_list=engine.categories)


@Route(routes, "/study_programs/")
class StudyPrograms:
    @Debug(name="StudyPrograms")
    def __call__(self, request):
        return "200 OK", render("study-programs.html.jinja", date=date.today())


@Route(routes, "/course/list/")
class CoursesListView:
    def __call__(self, request: dict) -> tuple[str, str]:
        logger.log("Course list")
        try:
            category = engine.find_category_by_id(int(request["request_params"]["id"]))
            return "200 OK", render(
                "course_list.html",
                objects_list=category.courses,
                name=category.name,
                id=category.id,
            )
        except KeyError:
            return "200 OK", "No courses have been added yet"


@Route(routes, "/course/create/")
class CreateCourseView:
    category_id = -1

    def __call__(self, request):
        if request["method"] == "POST":
            data = request["data"]

            name = data["name"]
            name = engine.decode_value(name)
            category = None

            if self.category_id != -1:
                category = engine.find_category_by_id(int(self.category_id))
                course = engine.create_course("record", name, category)
                engine.courses.append(course)

            return "200 OK", render(
                "course/create.html.jinja",
                objects_list=category.courses,
                name=category.name,
                id=category.id,
            )

        else:
            try:
                self.category_id = int(request["request_params"]["id"])
                category = engine.find_category_by_id(int(self.category_id))

                return "200 OK", render(
                    "course/create.html.jinja", name=category.name, id=category.id
                )
            except KeyError:
                return "200 OK", "No categories have been added yet"


@Route(routes, "/about/")
class AboutView:
    @Debug(name="About")
    def __call__(self, request: dict) -> tuple[str, str]:
        return "200 OK", render("about.html.jinja")


@Route(routes, "/category/list/")
class CategoryListView:
    def __call__(self, request: dict) -> tuple[str, str]:
        return "200 OK", render("category/list.html.jinja")


@Route(routes, "/category/create/")
class CreateCategoryView:
    def __call__(self, request):
        if request["method"] == "POST":
            data = request["data"]

            name = data["name"]
            name = engine.decode_value(name)

            category_id = data.get("category_id")

            category = None
            if category_id:
                category = engine.find_category_by_id(int(category_id))

            new_category = engine.create_category(name, category)
            engine.categories.append(new_category)

            return "200 OK", render("index.html.jinja", objects_list=engine.categories)
        else:
            categories = engine.categories
            return "200 OK", render("category/create.html.jinja", categories=categories)


@Route(routes, "/course/copy/")
class CopyCourseView:
    def __call__(self, request):
        request_params = request["request_params"]

        try:
            name = request_params["name"]
            old_course = engine.get_course(name)
            if old_course:
                new_name = f"copy_{name}"
                new_course = old_course.clone()
                new_course.name = new_name
                engine.courses.append(new_course)

            return "200 OK", render(
                "course/create.html.jinja",
                objects_list=engine.courses,
                name=new_course.category.name,
            )
        except KeyError:
            return "200 OK", "No courses have been added yet"


@Route(routes, "/student/list")
class StudentListView(ListView):
    queryset = engine.students
    template_name = "student_list.html"


@Route(routes, "/student/create")
class StudentCreateView(CreateView):
    template_name = "create_student.html"

    def create_obj(self, data: dict):
        name = data["name"]
        name = engine.decode_value(name)
        new_obj = engine.create_user("student", name)
        engine.students.append(new_obj)


@Route(routes, "/student/add")
class AddStudentByCourseCreateView(CreateView):
    template_name = "add_student.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["courses"] = engine.courses
        context["students"] = engine.students
        return context

    def create_obj(self, data: dict):
        course_name = data["course_name"]
        course_name = engine.decode_value(course_name)
        course = engine.get_course(course_name)
        student_name = data["student_name"]
        student_name = engine.decode_value(student_name)
        student = engine.get_student(student_name)
        course.add_student(student)


@Route(routes, "/api/")
class CourseAPI:
    @Debug(name="CourseAPI")
    def __call__(self, request):
        return "200 OK", BaseSerializer(engine.courses).save()


class NotFoundView:
    def __call__(self, request: dict) -> tuple[str, str]:
        return "404 Not Found", "<h1>404 Page Not Found</h1>"
