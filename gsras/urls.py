from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path("", views.index, name='index'),
    path("news/<int:id>/", views.see_full_news),
    path("main_page/", views.main_page, name='main_page'),
    path("dataselect/", views.dataselect, name='dataselect'),
    path("station/", views.station, name='station'),
    path("geofrom", views.geoform, name='geofrom'), path('captcha/', include('captcha.urls')),
    path("req_form", views.requsets_list, name = 'req_form'),
    path("structure", views.struct, name= "structure"),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [path('captcha/', include('captcha.urls')),]