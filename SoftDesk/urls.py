from django.contrib import admin
from django.urls import include, path
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from projects.views import ProjectViewset, IssueViewset, ContributorsViewset, CommentViewset
from users.views import SignupViewset


projects_router = routers.SimpleRouter()
projects_router.register(r'projects/?', ProjectViewset, basename='projects')

users_router = routers.NestedSimpleRouter(projects_router, r'projects/?', lookup='projects', trailing_slash=False)
users_router.register(r'users/?', ContributorsViewset, basename='users', )

issues_router = routers.NestedSimpleRouter(projects_router, r'projects/?', lookup='projects', trailing_slash=False)
issues_router.register(r'issues/?', IssueViewset, basename='issues')

comments_router = routers.NestedSimpleRouter(issues_router, r'issues/?', lookup='issues', trailing_slash=False)
comments_router.register(r'comments/?', CommentViewset, basename='comments', )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/api-auth/', include('rest_framework.urls')),
    path('api/signup/', SignupViewset.as_view(), name='signup'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/', include(projects_router.urls)),
    path('api/', include(users_router.urls)),
    path('api/', include(issues_router.urls)),
    path('api/', include(comments_router.urls)),
]
