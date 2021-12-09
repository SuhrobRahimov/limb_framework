from limb_framework.statuses import Status
from limb_framework.renderer import Render


class UserPage:
    def __call__(self, *args, **kwargs):
        data = {
            'title': "Личный кабинет пользователя",
            'h1': "Личный кабинет пользователя",
        }
        cur_render = Render(Status.HTTP_200_OK, 'user_page/index.html', data=data)
        return cur_render()


def user_page2():
    status = '200 OK'
    response_type = [('Content-Type', 'text/html')]
    response = [b"User page 2"]
    return status, response_type, response
