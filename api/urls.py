from django.urls import path
from .views.answer_views import Answers, AnswerDetail
from .views.survey_views import Surveys, SurveyDetail
from .views.question_views import Questions, QuestionDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    path('surveys/', Surveys.as_view(), name='surveys'),
    path('surveys/<int:pk>/', SurveyDetail.as_view(), name='survey_detail'),
    path('questions/', Questions.as_view(), name='questions'),
    path('questions/<int:pk>/', QuestionDetail.as_view(), name='question_detail'),
    path('answers/', Answers.as_view(), name='questions'),
    path('answers/<int:pk>/', AnswerDetail.as_view(), name='question_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
