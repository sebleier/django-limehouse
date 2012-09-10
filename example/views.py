from django.shortcuts import render
from blog.models import Entry


def homepage(request):
    entries = Entry.objects.all()
    return render(request, 'homepage.html', {'entries': entries})