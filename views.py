from nick_framework.templator import render


def index_view(request: dict) -> tuple[str, str]:
    return "200 OK", render("index.html.jinja")


def examples_view(request: dict) -> tuple[str, str]:
    return "200 OK", render("examples.html.jinja")


def contact_view(request: dict) -> tuple[str, str]:
    return "200 OK", render("contact.html.jinja")


def another_view(request: dict) -> tuple[str, str]:
    return "200 OK", render("another_page.html.jinja")


def page_view(request: dict) -> tuple[str, str]:
    return "200 OK", render("page.html.jinja")


def not_found_404_view(request: dict) -> tuple[str, str]:
    return "404 Not Found", "<h1>404 Page Not Found</h1>"
