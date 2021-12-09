from limb_framework.statuses import Status
from limb_framework.renderer import Render


class About:
    def __call__(self, *args, **kwargs):
        data = {
            'title': "Информация",
            'h1': "О портале Limb Catalogs",
            'data': {
                'vendors': [
                    'Kamaz', 'Komatsu', 'Liebherr',
                    'Atlas Copco', 'Caterpillar', 'Epiroc',
                    'Hanwha', 'Knelson'
                ]
            }
        }
        cur_render = Render(Status.HTTP_200_OK, 'about_page/index.html', data=data)
        return cur_render()
