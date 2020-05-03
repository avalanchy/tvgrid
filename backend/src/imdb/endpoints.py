from rest_framework import viewsets

from imdb.models import Title
from imdb.serializers import TitleSerializer


class TitleEndpoint(viewsets.ModelViewSet):
    queryset = Title.objects.prefetch_related("episodes__title__rating")
    serializer_class = TitleSerializer
