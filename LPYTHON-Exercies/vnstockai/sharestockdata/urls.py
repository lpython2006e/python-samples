from django.urls import path,include

from .views import testdata
app_name='sharestockdata'
urlpatterns = [
    path('', testdata.as_view(), name='test-data'),
]