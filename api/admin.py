from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Userstype)
class UserstypeAdmin(admin.ModelAdmin):
    list_display = ['user_type', 'description']


@admin.register(Account)
class UsersmemberAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname','email', 'user_type', 'is_active', 'is_staff']


@admin.register(FitnessProgram)
class FitnessProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'duree', 'target']

@admin.register(FitnessProgramsComment)
class FitnessProgramsCommentAdmin(admin.ModelAdmin):
    list_display = ['account','fitprog', 'comment','created_on']

@admin.register(UsersFitnessPrograms)
class UsersFitnessProgramsAdmin(admin.ModelAdmin):
    ordering = ('-joined_at',)
    list_display = ['account', 'fitprog', 'joined_at']

@admin.register(FitnessProgramsRating)
class FitnessProgramsRatingAdmin(admin.ModelAdmin):
    list_display = ['account', 'fitprog', 'stars']

@admin.register(AccountRating)
class AccountRatingAdmin(admin.ModelAdmin):
    ordering =  ('-rating_date',)
    list_display = ['account', 'account_to_rate', 'stars', 'rating_date']



@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['account', 'title', 'published', 'created_on']


@admin.register(BlogRating)
class BlogRatingAdmin(admin.ModelAdmin):

    list_display = ['account', 'blog', 'stars', 'rating_date']
    list_filter = ['account', 'blog', 'stars']


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['blog','account', 'created_on']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['account','title', 'fitprog', 'created_on', 'workout_type']


@admin.register(WorkoutsRating)
class WorkoutRatingAdmin(admin.ModelAdmin):

    list_display = ['account', 'workout', 'stars', 'rating_date']
    list_filter = ['account', 'workout', 'stars']

@admin.register(WorkoutComment)
class WorkoutCommentAdmin(admin.ModelAdmin):
    list_display = ['workout','account', 'created_on']
