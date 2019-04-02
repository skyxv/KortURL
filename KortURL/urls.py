"""KortURL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from api import urls as api_urls
from apps.users import views as user_views
from apps.pages import views as page_views
from apps.urls import views as url_views


urlpatterns = [
    path('', url_views.ShortenUrl.as_view(), name="index"),
    path('api/', include(api_urls, namespace='api')),
    path('login/', user_views.Login.as_view(), name="login"),
    path('logout/', user_views.Logout.as_view(), name="logout"),
    path('shorten/', url_views.ShortenUrl.as_view(), name="shorten"),
    path('reduce/', url_views.RevertUrl.as_view(), name="reduce"),
    path('docs/', page_views.Doc.as_view(), name="docs"),
    path('link_maps/', page_views.History.as_view(), name="link_maps"),
    path('history/', page_views.LinkMapView.as_view(), name="history"),
    path('history/<slug:code>/', page_views.HistoryDetail.as_view(), name="history_detail"),

    path('admin/', admin.site.urls),

]
