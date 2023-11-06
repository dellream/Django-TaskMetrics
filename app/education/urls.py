from django.urls import path
from . import views

app_name = 'education'

urlpatterns = [
    # Курсы
    path('courses_list/',
         views.ManageCourseListView.as_view(),
         name='manage_course_list'),
    path('create/',
         views.CourseCreateView.as_view(),
         name='course_create'),
    path('<pk>/edit/',
         views.CourseUpdateView.as_view(),
         name='course_edit'),
    path('<pk>/delete/',
         views.CourseDeleteView.as_view(),
         name='course_delete'),

    # Модули
    path('<pk>/module/',
         views.CourseModuleUpdateView.as_view(),
         name='course_module_update'),

    # Контент
    path('module/<int:module_id>/content/<model_name>/create/',
         views.CourseModuleUpdateView.as_view(),
         name='module_content_create'),
    path('module/<int:module_id>/content/<model_name>/<id>/',
         views.ContentCreateUpdateView.as_view(),
         name='module_content_update'),
    path('content/<int:id>/delete/',
         views.ContentDeleteView.as_view(),
         name='module_content_delete'),
]
