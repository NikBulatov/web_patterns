import views

routes = {
    "/": views.IndexView(),
    "/about/": views.AboutView(),
    "/courses-list/": views.CoursesListView(),
    "/create-course/": views.CreateCourseView(),
    "/create-category/": views.CreateCategoryView(),
    "/category-list/": views.CategoryListView(),
    "/copy-course/": views.CopyCourseView(),
}
