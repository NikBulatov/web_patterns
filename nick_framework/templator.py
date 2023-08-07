from os import path
from jinja2 import FileSystemLoader, environment
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
    env = environment.Environment()
    env.loader = FileSystemLoader(path.abspath(folder))
    template = env.get_template(template_name)
    return template.render(**kwargs)


if __name__ == "__main__":
    output_test = render("index.html.jinja", object_list=[{"name": "Leo"}, {"name": "Kate"}])
    print(output_test)
