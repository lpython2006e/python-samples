from django.urls import path

from . import views

urlpatterns = [
    path('', views.livestockclawler_home, name='home'),
    path('function/', views.login_required, name='function_login_required'),
    path('no_login_function/', views.no_login_required, name='function_no_login_required'),
    path('class/', views.RestrictedView.as_view(), name='restricted_view'),
    # path('decorated_class/', views.DecoratedRestrictedView.as_view(), name='decorated_restricted_view')

    path('can_view_stock/', views.can_view_stock, name='can_view_stock'),
]