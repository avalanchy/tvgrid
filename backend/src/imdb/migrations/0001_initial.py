# Generated by Django 3.0.2 on 2020-01-06 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.CharField(help_text='Alphanumeric unique identifier of the title.', max_length=255, primary_key=True, serialize=False)),
                ('title_type', models.CharField(choices=[('movie', 'Movie'), ('short', 'Short'), ('tvEpisode', 'Tv Episode'), ('tvMiniSeries', 'Tv Mini Series'), ('tvMovie', 'Tv Movie'), ('tvSeries', 'Tv Series'), ('tvShort', 'Tv Short'), ('tvSpecial', 'Tv Special'), ('video', 'Video'), ('videoGame', 'Video Game')], help_text='The type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc).', max_length=500)),
                ('primary_title', models.CharField(help_text='The more popular title / the title used by the filmmakers on promotional materials at the point of release.', max_length=500)),
                ('original_title', models.CharField(help_text='Original title, in the original language.', max_length=500)),
                ('is_adult', models.BooleanField(help_text='Non-adult/adult title.')),
                ('start_year', models.CharField(blank=True, help_text='Represents the release year of a title. In the case of TV Series, it is the series start year (YYYY).', max_length=4, null=True)),
                ('end_year', models.CharField(blank=True, help_text='TV Series end year. \\N for all other title types. (YYYY)', max_length=4, null=True)),
                ('runtime_minutes', models.CharField(blank=True, help_text='Primary runtime of the title, in minutes.', max_length=10, null=True)),
                ('genres', models.CharField(blank=True, help_text='Includes up to three genres associated with the title.', max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('title', models.OneToOneField(help_text='Alphanumeric identifier of episode.', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='imdb.Title')),
                ('average_rating', models.FloatField(help_text='Weighted average of all the individual user ratings.')),
                ('num_votes', models.IntegerField(help_text='Number of votes the title has received.')),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('title', models.OneToOneField(help_text='Alphanumeric identifier of episode.', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='imdb.Title')),
                ('season_number', models.IntegerField(blank=True, help_text='Season number the episode belongs to.', null=True)),
                ('episode_number', models.IntegerField(blank=True, help_text='Episode number of the tconst in the TV series.', null=True)),
                ('parent_title', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='imdb.Title')),
            ],
        ),
    ]
