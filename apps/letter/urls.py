from django.urls import path
from .views import root, add_letter, archive

urlpatterns = [
    path('dashboard/', root, name="index"),
    path('dashboard/add-letter', add_letter, name="add_letter"),
    path('dashboard/archives/', archive, name='archives'),
]
