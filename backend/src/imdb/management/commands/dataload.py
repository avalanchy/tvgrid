import csv
import gzip
import os

import requests
from django.core.management.base import BaseCommand, CommandError

from ...models import IMDbBasics, IMDbEpisode, IMDbRatings


def download_file(url):
    """based on https://stackoverflow.com/a/16696317/1765615 added checking if
    file exists.
    """
    local_filepath = '/tmp/' + url.split('/')[-1]
    if os.path.exists(local_filepath):
        # file already exists
        return local_filepath
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    # filter out keep-alive new chunks
                    f.write(chunk)
    return local_filepath


def parse_bool(text):
    return bool(int(text))


def parse_nullable(text):
    if text == r'\N':
        return None
    return text


class Command(BaseCommand):
    help = "Load data from IMDb Datasets"

    def handle(self, *args, **options):
        basics_tsv_gz = download_file("https://datasets.imdbws.com/title.basics.tsv.gz")
        episode_tsv_gz = download_file("https://datasets.imdbws.com/title.episode.tsv.gz")
        ratings_tsv_gz = download_file("https://datasets.imdbws.com/title.ratings.tsv.gz")

        with gzip.open(basics_tsv_gz, "rt") as f:

            IMDbBasics.objects.all().delete()

            reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
            chunk = []

            for row in reader:
                if row["titleType"] not in [k for k, _ in IMDbBasics.TITLE_TYPES]:
                    continue

                basics = IMDbBasics(
                    tconst=row["tconst"],
                    title_type=row["titleType"],
                    primary_title=row["primaryTitle"],
                    original_title=row["originalTitle"],
                    is_adult=parse_bool(row["isAdult"]),
                    start_year=row["startYear"],
                    end_year=parse_nullable(row["endYear"]),
                    runtime_minutes=parse_nullable(row["runtimeMinutes"]),
                    genres=parse_nullable(row["genres"]),
                )

                chunk.append(basics)

                if len(chunk) == 999:
                    IMDbBasics.objects.bulk_create(chunk)
                    chunk = []
                    self.stdout.write(f'Saving 999 for row {reader.line_num}')
