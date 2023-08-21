from nick_framework.templator import render
from patterns.engine import Engine

engine = Engine()


class IndexView:
    def __call__(self, request: dict) -> tuple[str, str]:
        return "200 OK", render("index.html.jinja")


class CoursesListView:
    def __call__(self, request: dict) -> tuple[str, str]:
        return "200 OK", render("course/list.html.jinja")


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
                models = [engine.create_model(f"Something #{i}") for i in range(4)]
                course = engine.create_course("record", name, category, models)
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


class AboutView:
    def __call__(self, request: dict) -> tuple[str, str]:
        return "200 OK", render("about.html.jinja")


class CategoryListView:
    def __call__(self, request: dict) -> tuple[str, str]:
        return "200 OK", render("category/list.html.jinja")


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

            return "200 OK", render(
                "category/create.html.jinja", objects_list=engine.categories
            )
        else:
            categories = engine.categories
            return "200 OK", render("category/create.html.jinja", categories=categories)


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


class NotFoundView:
    def __call__(self, request: dict) -> tuple[str, str]:
        return "404 Not Found", "<h1>404 Page Not Found</h1>"
