from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    """Стандартный пагинатор, с определенными атрибутами
    'page_size_query_param' и 'page_size'.
    """
    page_size_query_param = 'limit'
    page_size = 2
