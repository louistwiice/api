from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import *
from .models import *
from rest_framework.authentication import TokenAuthentication


# Create your views here.

class UsersTypesREST(viewsets.ModelViewSet):
    serializer_class = UserstypeSerializer
    queryset = Userstype.objects.all()

    def create(self, request, *args, **kwargs):
        account = request.user

        if account.is_superuser != True:
            response = {'detail': "Not allowed to create a user type with your privilege"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserstypeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        account = request.user

        if account.is_superuser != True:
            response = {'detail': "Not allowed to delete a user type with your privilege"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            pk = kwargs['pk']
            Userstype.objects.get(id=pk).delete()
            return Response(status=status.HTTP_200_OK)


    def update(self, request, *args, **kwargs):
        account = request.user

        if account.is_superuser != True:
            response = {'detail': "Not allowed to update a user type with your privilege"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            pk = kwargs['pk']
            usertype = Userstype.objects.get(id=pk)
            serializer = UserstypeSerializer(usertype, data=request.data)
            if serializer.is_valid():
                serializer.update(instance=usertype, validated_data=request.data)

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def partial_update(self, request, *args, **kwargs):
        response = {'detail': 'Method \"PATCH\" not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class AccountREST(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


    def update(self, request, *args, **kwargs):
        account = request.user
        pk = kwargs['pk']

        if account.is_superuser == True or account.id == pk:
            account_to_update = Account.objects.get(id=pk)
            serializer = self.get_serializer(data= request.data)


            if serializer.is_valid():
                data = request.data.copy()
                data['user_type'] = Userstype.objects.get(id= request.data['user_type'] )
                serializer.update(instance=account_to_update, validated_data=data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            response = {'detail': "Forbidden to update another user with your privilege"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        account = request.user
        pk = kwargs['pk']
        account_to_delete = Account.objects.get(id=pk)

        if account == account_to_delete or account.is_staff or account.is_superuser:
            account_to_delete.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            response = {'detail': 'Unauthorized to delete account of another. Please check your privilege'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        response = {'detail': "Unable to list all users in this url. Please check Djoser url"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'detail': "Unable to create a user in this url. Please check Djoser url"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'detail': "Method \PATCH\ not allowed"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['POST'])
    def rate(self, request, pk=None):
        if 'stars' in request.data:
            account_rated = Account.objects.get(id=pk)
            stars = request.data['stars']
            account = request.user

            # This is to check if the user send a number, not a string
            try:
                int(stars)
            except Exception as err:
                response = {'detail': "stars should be only integer"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)


            try:
                rating = AccountRating.objects.get(account=account, account_to_rate=account_rated)

                rating.stars = stars
                rating.save()

                serializer = AccountRatingSerializer(rating, many=False)

                response = {'message': "Rating updated", 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

            except Exception as err:
                rating = AccountRating.objects.create(account=account, account_to_rate=account_rated, stars=stars)
                serializer = AccountRatingSerializer(rating, many=False)


                response = {'message': "Rating created", 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'detail': "You need to provide stars"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



    @action(detail=True, methods=['GET'])
    def program(self, request, pk=None):
        """
        This view returns a program associated to a user

        :param request:
        :return:
        """
        account_pk = Account.objects.get(id=pk)
        account = request.user

        if (not account.is_superuser and account == account_pk) or account.is_superuser:
            userprog = UsersFitnessPrograms.objects.filter(account=account_pk)
            serializer = UsersFitnessProgramsSerializer(userprog, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            response = {'detail': 'Not allowed'}
            return Response(response, status=status.HTTP_200_OK)




class FitnessProgramREST(viewsets.ModelViewSet):
    serializer_class = FitnessProgramSerializer
    queryset = FitnessProgram.objects.all()

    def create(self, request, *args, **kwargs):
        account = request.user

        if account.is_staff != True:
            response = {'detail': "Not allowed to create a fitness program with your privilege"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = FitnessProgramSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        account = request.user

        if account.is_staff != True:
            response = {'detail': "Not allowed to update a fitness program with your privilege"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            pk = kwargs['pk']
            fitprog = FitnessProgram.objects.get(id=pk)
            serializer = FitnessProgramSerializer(fitprog, data=request.data)

            if serializer.is_valid():
                serializer.update(instance=fitprog, validated_data=request.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        account = request.user

        if account.is_superuser != True or account.is_staff != True:
            response = {'detail': "Not allowed to delete a fitness program type with your privilege"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            pk = kwargs['pk']
            FitnessProgram.objects.get(id=pk).delete()
            return Response(status=status.HTTP_200_OK)


    def partial_update(self, request, *args, **kwargs):
        response = {'detail': "Method \PATCH\ not allowed"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['POST'])
    def rate_fitnessprogram(self, request, pk=None):
        if 'stars' in request.data:

            fitprog = FitnessProgram.objects.get(id=pk)
            stars = request.data['stars']

            #This is to check if the user send a number, not a string
            try:
                int(stars)
            except Exception as err:
                response = {'detail': "stars should be only integer"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            account = request.user

            try:
                rating = FitnessProgramsRating.objects.get(account=account, fitprog=fitprog)
                rating.stars = stars
                rating.save()
                serializer = FitnessProgramsRatingSerializer(rating, many=False)

                response = {'message': "Rating updated", 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except Exception as err:
                rating = FitnessProgramsRating.objects.create(account=account, fitprog=fitprog, stars=stars)
                serializer = FitnessProgramsRatingSerializer(rating, many=False)

                response = {'message': "Rating created", 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'detail': "You need to provide stars"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def comments_list(self, request, pk=None):
        """
        List alls comments specific to an posted blog
        :param request:
        :param pk:
        :return:
        """
        comments = FitnessProgramsComment.objects.filter(fitprog_id=pk)
        serializer = FitnessProgramsCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def comment_program(self, request, pk=None):
        if 'comment' in request.data:

            fitprog = FitnessProgram.objects.get(id=pk)
            coming_comment = request.data['comment']

            account = request.user

            comment = FitnessProgramsComment.objects.create(account=account, fitprog=fitprog, comment=coming_comment)
            serializer = FitnessProgramsCommentSerializer(comment, many=False)

            response = {'message': "Comment created", 'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'detail': "You need to provide a comment"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class FitnessProgramsCommentREST(viewsets.ModelViewSet):
    serializer_class = FitnessProgramsCommentSerializer
    queryset = FitnessProgramsComment.objects.all()


    def create(self, request, *args, **kwargs):
        account = request.user

        serializer = FitnessProgramsCommentSerializer(data=request.data)

        if serializer.is_valid():
            data = request.data.copy()
            data['account'] = account.id #We should copy the request data and edit it, so that every comment would be registered
            #in the name of the connected user

            serializer = FitnessProgramsCommentSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def update(self, request, *args, **kwargs):
        account = request.user
        pk = kwargs['pk']
        comment = FitnessProgramsComment.objects.get(id=pk)
        serializer = FitnessProgramsCommentSerializer(comment, data=request.data)

        if account == comment.account:
            if serializer.is_valid():
                fitprog = FitnessProgram.objects.get(id=request.data['fitprog'])

                data = request.data.copy()
                data['fitprog'] = fitprog
                serializer.update(instance=comment, validated_data=data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            response = {'detail': "You can't edit comment of another account"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        account = request.user
        pk = kwargs['pk']
        comment = FitnessProgramsComment.objects.get(id=pk)

        if account.is_superuser or account.is_staff or account == comment.account:
            comment.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            response = {'detail': "Not allowed to delete comment of another account with your privilege"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def partial_update(self, request, *args, **kwargs):
        response = {'detail': "Method \"PATCH\" not allowed"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)



class UsersFitnessProgramsREST(viewsets.ModelViewSet):
    serializer_class = UsersFitnessProgramsSerializer
    queryset = UsersFitnessPrograms.objects.all()


    def create(self, request, *args, **kwargs):
        account = request.user

        if account.is_superuser == True:
            if 'account' in request.data:
                serializer = UsersFitnessProgramsSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                response = {'detail': 'As you are a superuser, account is required'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        else:
            serializer = UsersFitnessProgramsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def update(self, request, *args, **kwargs):
        account = request.user
        pk = kwargs['pk']
        userprog = UsersFitnessPrograms.objects.get(id=pk)

        serializer = UsersFitnessProgramsSerializer(userprog, data=request.data)
        if account.is_superuser or account == userprog.account:

            if account.is_superuser and 'account' not in request.data:
                response = {'account': ['This field is required']}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                if serializer.is_valid():
                    fitprog = FitnessProgram.objects.get(id=request.data['fitprog'])

                    data = request.data.copy()
                    data['fitprog'] = fitprog  # We change the pk sent by an object, because the update doesn't work with a pk
                    if account.is_superuser:
                        account = Account.objects.get(id= request.data['account'])

                    data['account'] = account
                    serializer.update(instance=userprog, validated_data=data)

                    serializer = UsersFitnessProgramsSerializer(userprog, many=False)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            response = {'detail': "Unauthorized to edit program association of another user"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



    def destroy(self, request, *args, **kwargs):
        account = request.user
        pk = kwargs['pk']
        userprog = UsersFitnessPrograms.objects.get(id=pk)

        if account == userprog.account or account.is_superuser or account.is_staff:
            userprog.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            response = {'detail': 'Delete not allowed. Check your privilege'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def partial_update(self, request, *args, **kwargs):
        response = {'detail': "Method \"PATCH\" not allowed"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)




class FitnessProgramsRatingREST(viewsets.ModelViewSet):
    serializer_class = FitnessProgramsRatingSerializer
    queryset = FitnessProgramsRating.objects.all()


    def create(self, request, *args, **kwargs):
        account = request.user
        data = request.data.copy()
        data['account'] = account.id
        serializer = FitnessProgramsRatingSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        account = request.user
        pk = kwargs['pk']
        rating = FitnessProgramsRating.objects.get(id=pk)
        serializer =FitnessProgramsRatingSerializer(rating,data=request.data)

        if account == rating.account:
            if serializer.is_valid():
                data = request.data.copy()
                data['account'] = rating.account
                data['fitprog'] = rating.fitprog
                serializer.update(instance=rating, validated_data=data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {'detail': 'Unauthorized to edit rating of another account'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        account = request.user
        pk = kwargs['pk']
        rating = FitnessProgramsRating.objects.get(id=pk)

        if account == rating.account or account.is_staff:
            rating.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            response = {'detail': 'Unauthorized to delete rating of another account! Please check your privilege'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


def partial_update(self, request, *args, **kwargs):
        response = {'detail': "Method \"PATCH\" not allowed"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)



class AccountRatingsREST(viewsets.ModelViewSet):
    serializer_class = AccountRatingSerializer
    queryset = AccountRating.objects.all()

    def create(self, request, *args, **kwargs):
        account = request.user
        data = request.data.copy()
        data['account'] = account.id
        serializer = AccountRatingSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        account = request.user
        pk = kwargs['pk']
        rating = AccountRating.objects.get(id=pk)
        serializer =AccountRatingSerializer(rating,data=request.data)

        if account == rating.account:
            if serializer.is_valid():
                data = request.data.copy()
                data['account'] = rating.account
                data['account_to_rate'] = rating.account_to_rate
                serializer.update(instance=rating, validated_data=data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {'detail': 'Unauthorized to edit rating of another account'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        account = request.user
        pk = kwargs['pk']
        rating = AccountRating.objects.get(id=pk)

        if account == rating.account or account.is_staff:
            rating.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            response = {'detail': 'Unauthorized to delete rating of another account! Please check your privilege'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def partial_update(self, request, *args, **kwargs):
        response = {'detail': "Method \"PATCH\" not allowed"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)




class BlogREST(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()


    def list(self, request, *args, **kwargs):
        account = request.user

        if not account.is_superuser or not account.is_staff:
            blogs = Blog.objects.filter( Q(published=True) | Q(account=account) )
        else:
            blogs = Blog.objects.all()

        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def update(self, request, *args, **kwargs):
        account = request.user
        pk = kwargs['pk']
        blog = Blog.objects.get(id=pk)

        if account.is_superuser or account.is_staff or account == blog.account:
            serializer = self.get_serializer(instance= blog,data=request.data)
            if serializer.is_valid():
                data = request.data.copy()
                if account.is_superuser or account.is_staff:
                    data['account'] = blog.account

                serializer.update(instance=blog, validated_data=data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            response = {'detail': 'Unauthozired to edit article from another account'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



    def destroy(self, request, *args, **kwargs):
        account = request.user
        pk = kwargs['pk']
        blog = Blog.objects.get(id=pk)

        if not account.is_superuser or not account.is_staff:
            if account == blog.account:
                blog.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                response = {'detail': 'Unauthorize to delete blog from another account'}
                return Response( response, status=status.HTTP_400_BAD_REQUEST)
        else:
            blog.delete()
            return Response(status=status.HTTP_200_OK)


    def partial_update(self, request, *args, **kwargs):
        response = {'detail': "Method \"PATCH\" not allowed"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['POST'])
    def rate_blog(self, request, pk=None):
        if 'stars' in request.data:

            blog = Blog.objects.get(id=pk)
            stars = request.data['stars']

            # This is to check if the user send a number, not a string
            try:
                int(stars)
            except Exception as err:
                response = {'message': "stars should be only integer"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            account = request.user

            try:
                rating = BlogRating.objects.get(account=account, blog=blog)
                rating.stars = stars
                rating.save()
                serializer = BlogsRatingSerializer(rating, many=False)

                response = {'message': "Rating updated", 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except Exception as err:
                rating = BlogRating.objects.create(account=account, blog=blog, stars=stars)
                serializer = BlogsRatingSerializer(rating, many=False)

                response = {'message': "Rating created", 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': "You need to provide stars"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['GET'])
    def comment_list(self, request, pk=None):
        """
        List alls comments specific to an posted blog
        :param request:
        :param pk:
        :return:
        """
        comments = BlogComment.objects.filter(blog_id=pk)
        serializer = BlogCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['POST'])
    def comment_blog(self, request, pk=None):
        if 'comment' in request.data:

            blog = Blog.objects.get(id=pk)
            coming_comment = request.data['comment']

            account = request.user

            comment = BlogComment.objects.create(account=account, blog=blog, comment=coming_comment)
            serializer = BlogCommentSerializer(comment, many=False)

            response = {'message': "Comment created", 'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': "You need to provide a comment"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)




class BlogRatingREST(viewsets.ModelViewSet):
    serializer_class = BlogsRatingSerializer
    queryset = BlogRating.objects.all()

    def create(self, request, *args, **kwargs):
        account = request.user
        data = request.data.copy()

        if account.is_superuser or account.is_staff:
            if 'account' not in request.data:
                response = {'account': ['This field is required']}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("----------------------- 1")
            if account.is_superuser==False or account.is_staff==False:
                data['account']= account.id

            print("----------------------- 1")
            serializer= self.get_serializer(data = data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BlogCommentREST(viewsets.ModelViewSet):
    serializer_class = BlogCommentSerializer
    queryset = BlogComment.objects.all()


class WorkoutREST(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    queryset = Workout.objects.all()

    @action(detail=True, methods=['POST'])
    def rate_workout(self, request, pk=None):
        if 'stars' in request.data:

            workout = Workout.objects.get(id=pk)
            stars = request.data['stars']

            # This is to check if the user send a number, not a string
            try:
                int(stars)
            except Exception as err:
                response = {'message': "stars should be only integer"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            account = request.user

            try:
                rating = WorkoutsRating.objects.get(account=account, workout=workout)
                rating.stars = stars
                rating.save()
                serializer = WorkoutsRatingSerializer(rating, many=False)

                response = {'message': "Rating updated", 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except Exception as err:
                rating = WorkoutsRating.objects.create(account=account, workout=workout, stars=stars)
                serializer = WorkoutsRatingSerializer(rating, many=False)

                response = {'message': "Rating created", 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': "You need to provide stars"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['GET'])
    def comments_list(self, request, pk=None):
        comments = WorkoutComment.objects.filter(workout_id= pk)
        serializer = WorkoutCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['POST'])
    def comment_workout(self, request, pk=None):
        if 'comment' in request.data:

            workout = Workout.objects.get(id=pk)
            coming_comment = request.data['comment']

            account = request.user

            comment = WorkoutComment.objects.create(account=account, workout=workout, comment=coming_comment)
            serializer = WorkoutCommentSerializer(comment, many=False)

            response = {'message': "Comment created", 'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': "You need to provide a comment"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



class WorkoutRatingREST(viewsets.ModelViewSet):

    serializer_class = WorkoutsRatingSerializer
    queryset = WorkoutsRating.objects.all()


class WorkoutCommentREST(viewsets.ModelViewSet):

    serializer_class = WorkoutCommentSerializer
    queryset = WorkoutComment.objects.all()
