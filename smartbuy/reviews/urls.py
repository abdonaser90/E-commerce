from django.urls import path
from . import views

urlpatterns = [
    path('<int:pro_id>', views.addReview, name="addReview")
]