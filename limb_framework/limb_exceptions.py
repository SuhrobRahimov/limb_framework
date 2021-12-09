
class SettingsConfiguration(Exception):
    def __init__(self, message: str = "Настройки не сконфигурированы"):
        super().__init__(message)


class NoForRouter(Exception):
    def __init__(self, message: str = "Нет роутера"):
        super().__init__(message)


class NoTemplate(Exception):
    def __init__(self, message: str = "Указанный шаблон отсутствует"):
        super().__init__(message)
