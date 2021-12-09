import os
from jinja2 import Template
from limb_framework.limb_exceptions import *
from limb_framework.statuses import Status
import settings


class Render:
    def __init__(self, _status: int = Status.HTTP_404_NOT_FOUND,
                 _template: str = "", **kwargs):

        self._template: str = _template

        self.status = self.get_status(_status)
        self.content_type = self.get_content_type()
        self.kw = kwargs

    def get_status(self, status):
        if status == Status.HTTP_200_OK:
            return '200 OK'
        else:
            return '404 NOT FOUND'

    def get_content_type(self):
        if self._template.lower().endswith('.html'):
            return [('Content-Type', 'text/html')]
        elif self._template.lower().endswith('.css'):
            return [('Content-Type', 'text/css')]
        else:
            return [('Content-Type', 'text/html')]

    def __call__(self, *args, **kwargs) -> (str, list, list):
        return self.status, self.content_type, self.render(self._template, **self.kw)

    def render(self, template_path, **kwargs):
        codepage = 'utf-8'
        if 'MAIN_CODEPAGE' in dir(settings):
            codepage = settings.MAIN_CODEPAGE

        if not template_path.count('.css'):
            root_path = 'templates'
            if 'TEMPLATES_PATH' in dir(settings):
                root_path = settings.TEMPLATES_PATH

            template_path = os.path.join(root_path, template_path)
            if not os.path.exists(template_path):
                raise NoTemplate()

        with open(template_path, 'r', encoding='utf-8') as tmplt:
            template = Template(tmplt.read())

        result: str = template.render(**kwargs)
        return [result.encode(codepage)]

    def render_static(self, template_path, **kwargs):
        codepage = 'utf-8'
        if 'MAIN_CODEPAGE' in dir(settings):
            codepage = settings.MAIN_CODEPAGE

        if not os.path.exists(template_path):
            raise NoTemplate()

        with open(template_path, 'r', encoding='utf-8') as tmplt:
            template = Template(tmplt.read())

        result: str = template.render(**kwargs)
        return self.status, self.content_type, [result.encode(codepage)]


def render(template_path, **kwargs):
    r = Render(Status.HTTP_200_OK, template_path)
    return r.status, r.content_type, r.render(template_path, **kwargs)
