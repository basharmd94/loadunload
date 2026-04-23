from django.urls import path
from .views import home
from .views import load_unload
from .views import item
from .views import party
from .views import employee
from .views import category
from .views import expense
from .views import reports

app_name = 'load'

urlpatterns = [

    path('', home.index, name='index'),
# items
    path('create-item/', item.create_item, name='create-item'),
    path('edit-item/<str:code>/', item.create_item, name='edit-item'),
    path('list-item/', item.list_item, name='list-item'),
    path('delete-item/<str:code>/', item.delete_item, name='delete-item'),

# partys
    path('create-party/', party.create_party, name='create-party'),
    path('edit-party/<str:code>/', party.create_party, name='edit-party'),
    path('list-party/', party.list_party, name='list-party'),
    path('delete-party/<str:code>/', party.delete_party, name='delete-party'),
# load unload entry
    path('create-load-unload/', load_unload.create_load_unload, name='create-load-unload'),
    path('list-load-unload/', load_unload.list_load_unload, name='list-load-unload'),
    path('delete-load-unload/<str:pk>/', load_unload.delete_load_unload, name='delete-load-unload'),
    path('recent-loads/', load_unload.recent_loads, name='recent-loads'),
    path('recent-unloads/', load_unload.recent_unloads, name='recent-unloads'),

# employees
    path('create-employee/', employee.create_employee, name='create-employee'),
    path('edit-employee/<str:code>/', employee.create_employee, name='edit-employee'),
    path('delete-employee/<str:code>/', employee.delete_employee, name='delete-employee'),

# expense categories
    path('create-category/', category.create_category, name='create-category'),
    path('edit-category/<int:pk>/', category.create_category, name='edit-category'),
    path('delete-category/<int:pk>/', category.delete_category, name='delete-category'),

# expenses / GL
    path('create-expense/', expense.create_expense, name='create-expense'),
    path('list-gl/', expense.list_gl, name='list-gl'),
    path('delete-expense/<int:pk>/', expense.delete_expense, name='delete-expense'),

# reports
    path('financial-report/', reports.financial_report, name='financial-report'),
]
