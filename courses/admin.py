from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import (Author, Student, Video, Course, Comments)


# Register your models here.

@admin.register(Author)
class AuthorAdmin(OSMGeoAdmin):
    list_display = ('first_Name', 'last_Name', 'email')


@admin.register(Student)
class StudentAdmin(OSMGeoAdmin):
    list_display = ('first_Name', 'last_Name', 'email')


@admin.register(Video)
class VideoAdmin(OSMGeoAdmin):
    list_display = ('title', 'video_URL')


@admin.register(Course)
class CourseAdmin(OSMGeoAdmin):
    list_display = ('course_Name', 'specialist_area')


@admin.register(Comments)
class CommentsAdmin(OSMGeoAdmin):
    list_display = ('comment',)
