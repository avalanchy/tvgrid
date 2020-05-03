from django.db import models


class Title(models.Model):
    """Contains the basic information for titles.

    Source: title.basics.tsv.gz
    """

    class Type(models.TextChoices):
        MOVIE = "movie"
        SHORT = "short"
        TV_EPISODE = "tvEpisode"
        TV_MINI_SERIES = "tvMiniSeries"
        TV_MOVIE = "tvMovie"
        TV_SERIES = "tvSeries"
        TV_SHORT = "tvShort"
        TV_SPECIAL = "tvSpecial"
        VIDEO = "video"
        VIDEO_GAME = "videoGame"

    id = models.CharField(
        max_length=255,
        help_text="Alphanumeric unique identifier of the title.",
        primary_key=True,
    )

    title_type = models.CharField(
        max_length=500,
        help_text=(
            "The type/format of the title (e.g. movie, short, tvseries, "
            "tvepisode, video, etc)."
        ),
        choices=Type.choices,
    )

    primary_title = models.CharField(
        max_length=500,
        help_text=(
            "The more popular title / the title used by the filmmakers on "
            "promotional materials at the point of release."
        ),
    )

    original_title = models.CharField(
        max_length=500, help_text="Original title, in the original language.",
    )

    is_adult = models.BooleanField(help_text="Non-adult/adult title.")

    start_year = models.CharField(
        max_length=4,
        null=True,
        blank=True,
        help_text=(
            "Represents the release year of a title. In the case of "
            "TV Series, it is the series start year (YYYY)."
        ),
    )

    end_year = models.CharField(
        max_length=4,
        null=True,
        blank=True,
        help_text="TV Series end year. \\N for all other title types. (YYYY)",
    )

    runtime_minutes = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="Primary runtime of the title, in minutes.",
    )

    genres = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Includes up to three genres associated with the title.",
    )

    def __str__(self):
        return f"{self.primary_title} ({self.id})"


class Episode(models.Model):
    """Contains the tv episode information.

    Source: title.episode.tsv.gz
    """

    class Meta:
        ordering = ("season_number", "episode_number")

    title = models.OneToOneField(
        Title,
        help_text="Alphanumeric identifier of episode.",
        primary_key=True,
        on_delete=models.DO_NOTHING,
    )

    parent_title = models.ForeignKey(
        Title,
        on_delete=models.DO_NOTHING,
        related_name="episodes",
        db_constraint=False,  # IMDb dump contains nonexistent IDs
    )

    season_number = models.IntegerField(
        help_text="Season number the episode belongs to.", null=True, blank=True,
    )

    episode_number = models.IntegerField(
        help_text="Episode number of the tconst in the TV series.",
        null=True,
        blank=True,
    )

    def __str__(self):
        return (
            f"s{self.season_number or 0}e{self.episode_number or 0} ({self.title_id})"
        )


class Rating(models.Model):
    """Contains the IMDb rating and votes information for titles.

    Source: title.ratings.tsv.gz
    """

    title = models.OneToOneField(
        Title,
        help_text="Alphanumeric identifier of episode.",
        primary_key=True,
        on_delete=models.DO_NOTHING,
    )

    average_rating = models.FloatField(
        help_text="Weighted average of all the individual user ratings.",
    )

    num_votes = models.IntegerField(
        help_text="Number of votes the title has received.",
    )

    def __str__(self):
        return f"{self.average_rating} ({self.title_id})"
