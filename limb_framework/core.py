# -*- coding: utf-8 -*-
import os
import types
import importlib

from limb_framework.limb_exceptions import *
from limb_framework.renderer import Render
from limb_framework.statuses import Status


def not_found():
    status = '404 NOT FOUND'
    response_type = [('Content-Type', 'text/html')]
    response = [b"404 NOT FOUND"]
    return status, response_type, response


class Core:
    def __init__(self, settings):
        self.status = True
        self.error = ""

        self.settings = settings
        self.BASE_PATH: str = os.path.join(
            *os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])

        self.routers = {}
        self.get_main_router()

        # Подключаем статику
        self.static: list = []
        self.load_static()

    def __call__(self, environ, start_response) -> list:
        path = environ['PATH_INFO']

        if not path.endswith('/') and not path.count('.'):
            path += '/'

        view = None
        target = None
        if path.count('.'):
            # Если статика
            view = self.check_static(path)
            start_response(view[0], view[1])
            return view[2]
        else:
            start_route: str = '/'
            result_route: str = ''
            for route, r_target in self.routers.items():
                if not route.endswith('/'):
                    route += '/'

                if not route == '/':
                    route = ''.join([start_route, route])

                if route in path:
                    if route == '/' and path != '/':
                        continue

                    if len(route) > len(result_route):
                        result_route = route
                        target = r_target

            if target is None:
                status, response_type, response = not_found()
                start_response(status, response_type)
                return response

            # print(result_route, path)
            module = self.import_module(target)
            if isinstance(module, types.ModuleType):
                # print("Success", route)
                view = self.parse_router(result_route, path, module)
            elif isinstance(module, types.FunctionType):
                view = module

        if isinstance(view, types.FunctionType) or isinstance(target, object):
            status, response_type, response = view()
        else:
            status, response_type, response = not_found()

        if isinstance(response, str):
            response = response.encode('utf-8')

        start_response(status, response_type)
        return response

    def get_main_router(self) -> None:
        if 'WS_ROOT' not in dir(self.settings):
            self.error_reaction('Не сконфигурированы настройки: нет перменной WS_ROOT')
            raise SettingsConfiguration(self.error)

        if not self.settings.WS_ROOT.get('main'):
            self.error_reaction('Не настроен роутер: нет main')
            raise NoForRouter(self.error)

        main_router = self.settings.WS_ROOT.get('main')
        module = self.routers = self.import_module(os.path.join(main_router, 'routers'))

        if 'router' not in dir(module):
            self.error_reaction('Не настроен роутер')
            raise NoForRouter(self.error)
        self.routers = module.router

    def parse_router(self, start_route, path, module):
        if 'router' not in dir(module):
            self.error_reaction('Не настроен роутер')
            raise NoForRouter(self.error)

        # app_path: str = '.'.join(module.__name__.split('.')[:-1])

        # result_route: str = ''
        target = None
        for route, r_target in module.router.items():
            if not route.endswith('/'):
                route += '/'

            route = ''.join([start_route, route])
            while route.count('//'):
                route = route.replace('//', '/')

            # print(2, route, path)

            if route == path:
                # result_route = route
                target = r_target

        if isinstance(target, types.FunctionType) or isinstance(target, object):
            return target
        else:
            return not_found

    def error_reaction(self, mess: str) -> None:
        self.error = mess
        self.status = False

    def import_module(self, path):
        if not path.count('\\') or not path.count('/'):
            path = path.split('.')
            path = os.path.join(*path)

        if not os.path.exists('.'.join([path, 'py'])):
            self.error_reaction('Не найден файл ' + path + '.py')
            raise NoForRouter(self.error)

        module_path = '.'.join(path.split('\\'))
        print(module_path)
        module = importlib.import_module(module_path)

        return module

    def load_static(self):
        path = 'templates/styles/'
        if 'STATIC_PATH' not in dir(self.settings):
            path = self.settings.STATIC_PATH
            if not path.endswith('/'):
                path = path + '/'

        path = os.path.join('./', path)
        if os.path.exists(path):
            self.static.append(path)

    def check_static(self, file):

        file = os.path.basename(file)
        path: str = None
        for p in self.static:
            p = os.path.join(p, file)

            while p.count('//'):
                p = p.replace('//', '/')

            print(p)
            if os.path.exists(p):
                path = p
                break

        if path is None:
            return not_found()

        cur_render = Render(Status.HTTP_200_OK, path)
        return cur_render()






