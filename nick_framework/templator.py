from os import path
from jinja2 import Template
from config import DEV_CONFIG


def render(
    template_name: str, folder: str = DEV_CONFIG.TEMPLATES_PATH, **kwargs
) -> str:
    """
    Render template body for HTML page

    :param folder: templates directory
    :param template_name:
    :param kwargs: arguments for template
    :return:
    """
    with open(path.join(folder, template_name), "r", encoding="utf-8") as f:
        template = Template(f.read())
    return template.render(**kwargs)


if __name__ == "__main__":
    output_test = render("index.html", object_list=[{"name": "Leo"}, {"name": "Kate"}])
    print(output_test)
