from django.urls import path

from apps.main.views import IncrementView

app_name = 'main'

urlpatterns = [
    path('', IncrementView.as_view(), name='increment'),
]
