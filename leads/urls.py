from django.urls import path
from .views import (
    lead_list,
    lead_detail,
    lead_create,
    lead_update,
    lead_delete,
    LeadListView,
    LeadDetailView,
    LeadCreateView,
    LeadUpdateView,
    LeadDeleteView,
    AssignAgentView,
    CatetoryListView,
    CatetoryDetailView,
    LeadCategoryUpdateView,
    LeadCategoryCreateView,
    LeadCategoryEditView,
    LeadCategoryDeleteView
)

app_name = "leads"

urlpatterns = [
    path('',LeadListView.as_view(),name="lead-list"),
    path('<int:pk>/',LeadDetailView.as_view(),name="lead-detail"),
    path('<int:pk>/update/',LeadUpdateView.as_view(),name="lead-update"),
    path('<int:pk>/delete/',LeadDeleteView.as_view(),name="lead-delete"),
    path('<int:pk>/assign-agent/',AssignAgentView.as_view(),name="assign-agent"),
    path('<int:pk>/category-update/',LeadCategoryUpdateView.as_view(),name="category-update"),
    path('create/',LeadCreateView.as_view(),name="lead-create"),
    path('create-category/',LeadCategoryCreateView.as_view(),name="category-create"),
    path('categories/',CatetoryListView.as_view(),name="category-list"),
    path('<int:pk>/category-detail/',CatetoryDetailView.as_view(),name="category-detail"),
    path('<int:pk>/category-edit/',LeadCategoryEditView.as_view(),name="category-edit"),
    path('<int:pk>/category-delete/',LeadCategoryDeleteView.as_view(),name="category-delete"),
]