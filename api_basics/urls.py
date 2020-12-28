from django.urls import path,include
from .views import (ArticleAPIView,article_detail,GenericAPIListView,GenericAPIDetailView,ArticleViewSet,
                    ArticleModelViewSet)

from rest_framework.routers import DefaultRouter

router1=DefaultRouter()
router2=DefaultRouter()
router1.register('article',ArticleViewSet,basename='article')
router2.register('model-article',ArticleModelViewSet,basename='a')

urlpatterns = [
    path('article/',ArticleAPIView.as_view()),
    path('article/<int:pk>/',article_detail),
    path('generic/article/<int:id>/',GenericAPIDetailView.as_view()),
    path('generic/article/',GenericAPIListView.as_view()),
    path('viewset/',include(router1.urls)),
    path('',include(router2.urls)),

]