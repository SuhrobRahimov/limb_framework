# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server

import settings
from limb_framework.core import Core

app = Core(settings)

with make_server(settings.HOST, settings.PORT, app) as httpd:
    print(f"Запуск на порту {settings.PORT}...")
    httpd.serve_forever()
