from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationAPIView, UserLoginAPIView, AllEventListAPIView, EventLikeAPIView, UserEventListAPIView, CreateEventAPIView

urlpatterns = [
    path('users/', UserRegistrationAPIView.as_view(), name='users'),
    # path('token/', UserLoginAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-event/', CreateEventAPIView.as_view(), name='create_event'),
    path('user-events/', UserEventListAPIView.as_view()),
    path('events/', AllEventListAPIView.as_view()),
    path('events/<int:event_id>/', EventLikeAPIView.as_view()),
]
