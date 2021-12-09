from limb_framework.renderer import Render
from limb_framework.statuses import Status


class Index:
    def __call__(self, *args, **kwargs):
        data = {
            'title': "Главная страница",
            'h1': "Новости компании Limb Catalogs",
            'news': [
                {'id': 2, 'title': 'Ценообразование', 'data': '09.12.2021',
                 'text': 'Очень скоро мы представим вам прайс наших услуг'},
                {'id': 1, 'title': 'Мы открылись!', 'data': '09.12.2021',
                 'text': 'Объявляем об открытии нашего портала!'},

            ]
        }
        cur_render = Render(Status.HTTP_200_OK, 'main_page/index.html', data=data)
        return cur_render()
