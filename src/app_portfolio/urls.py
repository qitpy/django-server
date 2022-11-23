"""
URL mapping for user API
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_portfolio import views

app_name = 'app_portfolio'

router = DefaultRouter()
router.register('access-frequency',
                views.PortfolioAccessFrequencyView,
                basename='AccessFrequency')
router.register('message',
                views.PortfolioMessageViewSet,
                'leave-message')

urlpatterns = [
    path('', include(router.urls))
]
