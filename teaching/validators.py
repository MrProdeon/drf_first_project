from rest_framework import serializers


def youtube_validator(link):
    if "youtube.com" not in link:
        raise serializers.ValidationError(
            'Ссылка на видео должна содержать "youtube.com"'
        )
