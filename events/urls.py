from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('events/', EventView.as_view(), name='eventList'),
    path('registerList/<int:event>/', EventRegistartionView.as_view()),
    path('eventregister/', registerView.as_view()),
    path('userattend/', EventAttendView.as_view()),
    path('conform/', EventConformView.as_view()),
    path("createevent/", EventCreateView.as_view()),
    path('updateevent/', EventEditView.as_view()),
    path('getUserRegisterEvents/', UserRegisterEvent.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
