from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render

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

