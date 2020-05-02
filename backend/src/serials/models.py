from django.db import models

from imdb.models import Title


class Serial(models.Model):

    imdb_title = models.ForeignKey(Title, on_delete=models.DO_NOTHING)
