from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from .views import *

urlpatterns = [

    path('login/', login),
    path('logout/', Logout.as_view()),
    path('signup/', Studentsignup.as_view()),
    path('photoupload/', StudentProfileView.as_view()),
    path("clubList/", ClubListView.as_view()),
    path("updateprofile/", StudentProfileView.as_view()),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
