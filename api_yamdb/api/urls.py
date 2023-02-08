from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet,
                    TitleViewSet, ReviewViewSet, GenreViewSet, UserViewSet,
                    UserSignUpViewSet, TokenCreateViewSet)

app_name = 'api'

class NoPutRouter(DefaultRouter):
    """
    Кастомный роутер без 'PUT'.
    """
    def get_method_map(self, viewset, method_map):
        allowed_methods = super().get_method_map(viewset, method_map)
        if 'put' in allowed_methods.keys():
            del allowed_methods['put']
        return allowed_methods

router_v1 = NoPutRouter()

router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', UserSignUpViewSet.as_view()),
    path('v1/auth/token/', TokenCreateViewSet.as_view()),
]
