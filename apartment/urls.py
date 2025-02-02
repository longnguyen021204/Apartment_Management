from rest_framework import routers
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apartment import views, admin

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'vehicles', views.VehicleViewSet)
router.register(r'locker_items', views.LockerItemViewSet)
router.register(r'feedbacks', views.FeedbackViewSet)
router.register(r'surveys', views.SurveyViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]