from rest_framework import serializers
from .models import *
from rest_framework.authtoken.models import Token


class UserstypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userstype
        fields = ['id','user_type']

class FitnessProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = FitnessProgram
        fields = ['id', 'name', 'duree', 'target', 'description', 'number_of_rating', 'avg_rating', 'number_of_comments']


class FitnessProgramsCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = FitnessProgramsComment
        fields = ['id', 'account', 'fitprog', 'comment', 'created_on']
        extra_kwargs ={'account': {'required': False}}


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'firstname', 'lastname', 'password', 'sexe', 'is_active', 'phone',  'user_type', 'number_of_rating', 'avg_rating']
        extra_kwargs ={
            'password': {'write_only': True, 'required': True},
        }


    def create(self, validated_data):
        #We create a user
        account = Account.objects.create_user(**validated_data)

        #We create a token for the user because, we enable connexion with rest_framework token
        Token.objects.create(user=account)

        return account



class UsersFitnessProgramsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsersFitnessPrograms
        fields = ['id', 'account', 'fitprog', 'joined_at']
        extra_kwargs = {'account': {'required': False}}


class FitnessProgramsRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = FitnessProgramsRating
        fields = ['id','account', 'fitprog', 'stars', 'rating_date']
        extra_kwargs = {'account': {'required': False}}


class AccountRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountRating
        fields = ['id', 'account', 'account_to_rate', 'stars', 'rating_date']
        extra_kwargs = {'account': {'required': False}}



class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields =  ['id', 'account', 'title', 'content', 'created_on', 'last_updated', 'tags', 'published', 'source', 'number_of_rating', 'avg_rating', 'number_of_comments']


class BlogsRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogRating
        fields = ['id', 'account', 'blog', 'stars', 'rating_date']
        extra_kwargs = {'account': {'required': False}}



class BlogCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogComment
        fields = ['id', 'account', 'blog', 'comment', 'created_on']

class WorkoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workout
        fields = ['id', 'account', 'fitprog', 'title', 'about', 'created_on', 'price', 'nb_of_weeks', 'day_per_week', 'difficulty', 'body_focus', 'equipments', 'training_type', 'workout_type', 'number_of_rating', 'avg_rating', 'number_of_comments']


class WorkoutsRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutsRating
        fields = ['id', 'account', 'workout', 'stars', 'rating_date']

class WorkoutCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutComment
        fields = ['id', 'account', 'workout', 'comment', 'created_on']