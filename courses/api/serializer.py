from rest_framework import serializers
from courses.models import Author, Video


class AuthorSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Author
        fields = ('author_ID','email', 'first_Name', 'last_Name', 'password', 'gender')
        extra_kwargs = {'password': {'write_only': True},
                        'author_ID': {'read_only': True}, }


class VideoSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Video
        field = ('video_ID', 'title', )


# class ObtainTokenSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
