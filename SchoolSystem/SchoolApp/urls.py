from django.urls import path
from .views import hod, login_page,logout_user ,dologin, student_list, student_detail, add_student, student_update, student_delete
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('', login_page, name='login_page'),
    path('dologin/',dologin, name='dologin'),
    path('logout/', logout_user, name='logout_user'),
    path('hod_home/',hod, name='hod_home'),
    path('student_list/', student_list, name='student_list'),
    path('student/<int:pk>/', student_detail, name='student_detail'),
    path('student/new/', add_student, name='add_student'),
    path('student/<int:pk>/edit/', student_update, name='student_update'),
    path('student/<int:pk>/delete/', student_delete, name='student_delete'),
] + static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)
