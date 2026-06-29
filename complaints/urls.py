from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.intro_view, name='intro'),
    path('cpmplaint_form',views.home_view,name='home'),
    path('helpline/', views.helpline_view, name='helpline'),
    path('success/<int:complaint_id>/', views.complaint_success_view, name='complaint_success'),
    path('download-pdf/<int:complaint_id>/', views.download_pdf_view, name='download_pdf'),
    path('directory/', views.helpline_directory_view, name='helpline_directory'),
    path('disposal-guide/', views.smart_disposal_guide_view, name='disposal_guide'),
    path('animal-hospitals/', views.animal_hospital_map_view, name='animal_hospitals'),
    path('api/search-clinics/', views.search_clinics_api, name='search_clinics_api'),
    path('api/geocode/', views.geocode_address_api, name='geocode_api'),
    path('problem_solutions/', views.problems_solutions_view, name='problem_solution'),
     path('surveys/', views.surveys_view, name='surveys'),
]

