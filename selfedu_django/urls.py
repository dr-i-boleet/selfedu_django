"""
URL configuration for selfedu_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import selfedu_django.settings
from dsp.views import pageNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dsp.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if selfedu_django.settings.DEBUG:
    urlpatterns += static(selfedu_django.settings.MEDIA_URL, document_root=selfedu_django.settings.MEDIA_ROOT)

handler404 = pageNotFound
