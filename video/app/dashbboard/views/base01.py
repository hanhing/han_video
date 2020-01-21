from django.shortcuts import render
from django.views.generic import View


class Base01(View):
    TEMPLATE = 'dashboard/base01.html'

    def get(self, request):
        return render(request, self.TEMPLATE)
