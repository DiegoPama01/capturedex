from django.urls import path

from .views import CaptureCalculationView


app_name = "capture"

urlpatterns = [
    path(
        "calculate/",
        CaptureCalculationView.as_view(),
        name="calculate",
    ),
]