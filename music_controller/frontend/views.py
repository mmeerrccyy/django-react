from django.shortcuts import render
from django.views.generic.base import View

# Create your views here.
class Index(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'frontend/index.html')