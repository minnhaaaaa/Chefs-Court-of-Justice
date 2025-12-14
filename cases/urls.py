from django.urls import path
from .views import (
    submit_case,
    view_approved_cases,
    vote_case,
    approve_case,
    delete_case,
    judge_view_all,
    edit_case,
    reject_case,
    view_approved_cases,
    vote_case,
    vote_results
)

urlpatterns = [
    path('submit/', submit_case),
    path('approved/', view_approved_cases),
    path('vote/<int:case_id>/', vote_case),
    path('<int:case_id>/results/', vote_results),
    path('judge/all/', judge_view_all),
    path('<int:case_id>/edit/', edit_case),
    path('<int:case_id>/approve/', approve_case),
    path('<int:case_id>/reject/', reject_case),
    path('<int:case_id>/delete/', delete_case),

]
