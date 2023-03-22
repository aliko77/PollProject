from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import Main

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", Main.as_view(), name="home"),
    path("polls/", include("apps.poll.urls")),
    path("anketler/", include("apps.public_poll.urls")),
    path("account/", include("apps.account.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
