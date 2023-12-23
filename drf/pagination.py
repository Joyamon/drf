from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    """
    普通分页，数据量越大性能越差
    """
    page_size = 5
    page_size_query_param = 'size'
    page_query_param = 'page'
    max_page_size = 20
