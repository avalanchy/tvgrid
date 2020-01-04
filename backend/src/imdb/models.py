from django.db import models


class IMDbBasics(models.Model):
    """Contains the basic information for titles.

    Source: title.basics.tsv.gz
    """
    TV_SERIES = 'tvSeries'
    TV_EPISODE = 'tvEpisode'
    TITLE_TYPES = (
        (TV_SERIES, "TV Series"),
        (TV_EPISODE, "TV Episode"),
    )

    tconst = models.CharField(
        max_length=255,
        help_text="Alphanumeric unique identifier of the title.",
    )

    title_type = models.CharField(
        max_length=255,
        help_text=(
            "The type/format of the title (e.g. movie, short, tvseries, "
            "tvepisode, video, etc)."
        ),
        choices=TITLE_TYPES,
    )

    primary_title = models.CharField(
        max_length=255,
        help_text=(
            "The more popular title / the title used by the filmmakers on "
            "promotional materials at the point of release."
        ),
    )

    original_title = models.CharField(
        max_length=255,
        help_text="Original title, in the original language.",
    )

    is_adult = models.BooleanField(help_text="Non-adult/adult title.")

    start_year = models.CharField(
        max_length=4,
        help_text=(
            "Represents the release year of a title. In the case of "
            "TV Series, it is the series start year (YYYY)."
        ),
    )

    end_year = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="TV Series end year. \\N for all other title types. (YYYY)",
    )

    runtime_minutes = models.CharField(
        max_length=255,
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
        return self.primary_title


class IMDbEpisode(models.Model):
    """Contains the tv episode information.

    Source: title.episode.tsv.gz
    """

    tconst = models.CharField(
        max_length=255,
        help_text="Alphanumeric identifier of episode.",
    )

    parent_tconst = models.CharField(
        max_length=255,
        help_text="Alphanumeric identifier of the parent TV Series.",
    )

    season_number = models.IntegerField(
        help_text="Season number the episode belongs to.")

    episode_number = models.IntegerField(
        help_text="Episode number of the tconst in the TV series.")


class IMDbRatings(models.Model):
    """Contains the IMDb rating and votes information for titles.

    Source: title.ratings.tsv.gz
    """
    tconst = models.CharField(
        max_length=255,
        unique=True,
        help_text="Alphanumeric unique identifier of the title.",
    )

    average_rating = models.FloatField(
        help_text="Weighted average of all the individual user ratings.",
    )

    num_votes = models.IntegerField(
        help_text="Number of votes the title has received.",
    )
