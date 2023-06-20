from typing import Union


class DAOEmployerMixin:
    # TODO запилить реализацию
    async def get_active_employers_by_id(self, employer_tg_id: int) -> Union[dict, bool]:
        """
        1) не удален
        :param employer_tg_id:
        :return:
        """
        # pass
        return {'company_name': 'Марктика',
                'email': '@mail',
                'phone': '+79132511727'}
