from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render


from sharestockdata.models import StockInfo
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


# def testper(request):
#     if request.user.has_perm('sharestockdata.can_views'):
#         print(request.user)


# content_type = ContentType.objects.get_for_model(StockInfo)
# permission = Permission.objects.create(
#     codename='can_views',
#     name='Can Views Stocks info',
#     content_type=content_type,
# )
# pass 1e3q2wadS

# Create your views here.
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


def livestockclawler_home(request):
    template = loader.get_template('home.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def no_login_required(request):
    return HttpResponse("You should not need be login to see this (method)")


@login_required
def login_required(request):
    return HttpResponse("You should be login to see this (method)")


@permission_required('sharestockdata.view_stockinfo')
def can_view_stock(request):
    return HttpResponse("You can view stock data")


# @method_decorator(login_required, name='dispatch')
# class DecoratedRestrictedView(TemplateView):
#     template_name = 'login_required.html'


class RestrictedView(LoginRequiredMixin, TemplateView):
    template_name = 'login_required.html'

