from rest_framework.pagination import PageNumberPagination

class FormPagination(PageNumberPagination):
    page_size = 10           # Number of items per page
    page_size_query_param = 'page_size'  # Allow clients to set page size by query param ?page_size=5
    max_page_size = 100       # Maximum limit for page size
