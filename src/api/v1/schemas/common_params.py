from fastapi.param_functions import Query


class Pagination:
    def __init__(
            self,
            number: int = Query(1, alias='page[number]', gt=0, description='Нужная страница (зависит от размера)'),
            size: int = Query(50, alias='page[size]', gt=0, description='Размер записей на странице')
    ):
        self.number = number
        self.size = size
