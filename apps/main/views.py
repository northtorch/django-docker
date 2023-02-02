from __future__ import annotations

from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView

from apps.main.models import CountData


class IncrementView(TemplateView):
    template_name = 'main/increment.html'

    def get_context_data(self, **kwargs: dict) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        count_data, _ = CountData.objects.get_or_create()
        context["current_count"] = count_data.count
        return context

    def post(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        count_data, _ = CountData.objects.get_or_create()
        count_data.count += 1
        count_data.save()
        return self.get(request=request, *args, **kwargs)
