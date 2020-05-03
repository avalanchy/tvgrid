from rest_framework import serializers

from imdb.models import Title, Episode


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = (
            "season_number",
            "episode_number",
            "primary_title",
            "average_rating",
        )

    primary_title = serializers.CharField(source="title.primary_title")

    average_rating = serializers.CharField(source="title.rating.average_rating")


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ("primary_title", "episodes")

    episodes = EpisodeSerializer(many=True, read_only=True)
