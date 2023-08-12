from django.urls import path
from courses.views import (CreateAuthorAPIView,
                           AuthorRetrieveUpdate, ObtainAuthorTokenView,
                           ObtainAuthorsView, ObtainStudentsView, LoginUserView)
from courses import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/author/create', CreateAuthorAPIView.as_view()),
    path('api/author/update/', AuthorRetrieveUpdate.as_view()),
    path('api/author/authenticate/', views.authenticate_author),
    path('api/author/verify/', ObtainAuthorTokenView.as_view()),
    path('api/author/get_authors', ObtainAuthorsView.as_view()),
    path('api/student/get_all_students', ObtainStudentsView.as_view()),
    path('api/user/sign_in', LoginUserView.as_view())
]