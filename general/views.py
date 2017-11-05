# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from general.models import *


def home(request):
	result = []
	for mc in Category.objects.filter(parent__isnull=True):
		cc = Category.objects.filter(parent=mc)
		cc = [ii.name for ii in cc]
		result += [(mc.name, mc.columns, cc)]
	return render(request, 'index.html', {'categories': result})

def login(request):
	return render(request, 'login.html')
