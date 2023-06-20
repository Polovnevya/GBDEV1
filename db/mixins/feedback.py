from ..types import DAOFeedback


class DAOFeedbackMixin:
    # TODO записать отклик в базу данных
    async def insert_or_update_vacancy_response(self, vacancy_response: DAOFeedback) -> None:
        pass
