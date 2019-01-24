from django.urls import path

from core import views

urlpatterns = [
    path('core/getcns/', views.GetCNS.as_view(), name='core.getcns'),
    path('list/<int:year>/<int:month>/<int:day>)/', views.PrintList.as_view(), name='core.print'),
    path('vacancy/', views.this_month, name='core.vacancy_all'),
    path('vacancy/<int:year>/<int:month>/', views.calendar, name='core.vacancy_month'),
    path('folder/', views.folder, name='core.folder'),
    path('tag/', views.tag, name='core.tag')
]
