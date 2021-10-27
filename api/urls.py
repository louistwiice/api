from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()

router.register(r'users', AccountREST, basename='users')
router.register(r'userstypes', UsersTypesREST)
router.register(r'programs', FitnessProgramREST)
router.register(r'programscomments', FitnessProgramsCommentREST)
router.register(r'usersprogram', UsersFitnessProgramsREST)
router.register(r'blogs', BlogREST)
router.register(r'blogcomments', BlogCommentREST)
router.register(r'workouts', WorkoutREST)
router.register(r'workoutcomments', WorkoutCommentREST)

router.register(r'programsrating', FitnessProgramsRatingREST)
router.register(r'accountrating', AccountRatingsREST)
router.register(r'blogsrating', BlogRatingREST)
router.register(r'workoutsrating', WorkoutRatingREST)



urlpatterns = [
    path('', include((router.urls, 'api_views'), namespace="api_views" )),
    path('auth/', include(('djoser.urls', 'djoser_auth'), namespace="djoser_auth") ),
    path('auth/', include(('djoser.urls.authtoken', 'djoser_token'), namespace='djoser_token') ),
]