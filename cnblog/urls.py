from django.contrib import admin
from django.urls import path, re_path, include

SOCIAL_AUTH_URL_NAMESPACE = 'social'

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^', include(('blog.urls', 'blog')))

]
