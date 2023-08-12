from rest_framework import serializers
from courses.models import (Author, Video, Student)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Author
        fields = ('author_ID', 'email', 'first_Name', 'last_Name', 'password', 'gender')
        extra_kwargs = {'password': {'write_only': True},
                        'author_ID': {'read_only': True}, }

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.groups.add("Author")
        instance.save()
        return instance


class VideoSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Video
        field = ('video_ID', 'title',)


class StudentSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Student
        fields = ('student_ID', 'email', 'first_Name', 'last_Name', 'password', 'gender')
        extra_kwargs = {'password': {'write_only': True},
                        'student_ID': {'read_only': True}, }

# class ObtainTokenSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
