# Generated by Django 3.0.2 on 2020-01-06 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='parent_title',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='episodes', to='imdb.Title'),
        ),
    ]
