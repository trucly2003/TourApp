from rest_framework.pagination import PageNumberPagination

class TourPaginator(PageNumberPagination):
    page_size = 2