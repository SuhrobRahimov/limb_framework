from limb_framework.statuses import Status
from limb_framework.renderer import Render


class ContactsView:
    def __call__(self, *args, **kwargs):
        data = {
            'title': "Контакты",
            'h1': "Контакты",
            'data': {
                'phones': [
                    {'id': 0, 'name': 'Ионов Валенрий Дронович',
                     'status': 'Директор',
                     'value': '+79081111111'},
                    {'id': 1, 'name': 'Васильев Василий Васильевич',
                     'status': 'Специалист по рекламе',
                     'value': '+79082222222'}
                ],
                'addresses': [
                    {'id': 0, 'value': 'Красноярск, ул. Мира, 24 оф. 206'}
                ]
            }
        }
        cur_render = Render(Status.HTTP_200_OK, 'contacts_page/index.html', data=data)
        return cur_render()
