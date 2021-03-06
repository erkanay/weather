from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    url(r'^login/$', views.UserLoginView.as_view(), name='login')
]

router = DefaultRouter()
router.register(r'weather', views.WeatherView, base_name='weather')
router.register(r'signup', views.UserSignupView, base_name='signup')

urlpatterns += router.urls
