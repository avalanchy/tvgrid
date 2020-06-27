import gzip
import os

import requests
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.transaction import atomic

from ...models import Title, Episode, Rating


class Command(BaseCommand):
    help = "Load data from IMDb Datasets"

    MODELS_AND_URLS = (
        (Title, "https://datasets.imdbws.com/title.basics.tsv.gz"),
        (Episode, "https://datasets.imdbws.com/title.episode.tsv.gz"),
        (Rating, "https://datasets.imdbws.com/title.ratings.tsv.gz"),
    )

    @staticmethod
    def download_file(url):
        """Function downloads large files in with requests with low memory
        usage.

        Based on https://stackoverflow.com/a/16696317/1765615.
        """
        filename = url.split("/")[-1]
        local_filepath = f"/tmp/{filename}"
        if os.path.exists(local_filepath):
            # file already exists
            return local_filepath
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filepath, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        # filter out keep-alive new chunks
                        f.write(chunk)
        return local_filepath

    @staticmethod
    def copy_to_table(filepath, model):
        """Function copies TSV file to PostgresSQL based model."""
        cursor = connection.cursor()
        with gzip.open(filepath, "rt") as f:
            f.readline()  # skip header line
            cursor.copy_from(
                file=f,
                table=model._meta.db_table,
                sep="\t",
                columns=[f.attname for f in model._meta.concrete_fields],
            )

    def handle(self, *args, **options):
        for i, (model, url) in enumerate(self.MODELS_AND_URLS, start=1):
            log_prefix = f"{i}/{len(self.MODELS_AND_URLS)} {model.__name__}\t"

            self.stdout.write(f"{log_prefix} Downloading data dump {url}.")
            filepath = self.download_file(url)

            with atomic():
                self.stdout.write(f"{log_prefix} Deleting existing data.")
                model.objects.all().delete()

                self.stdout.write(f"{log_prefix} Loading data from {filepath}.")
                self.copy_to_table(filepath, model)

        self.stdout.write("Done.")
