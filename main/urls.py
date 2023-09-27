from django.urls import path
from main.views import show_main, create_item, show_html, show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user, add_item, decrease_item, remove_item

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-item', create_item, name='create_item'),
    path('html/', show_html, name='show_html'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_item/<int:id>', add_item, name='add_item'),
    path('decrease_item/<int:id>', decrease_item, name='decrease_item'),
    path('remove_item/<int:id>', remove_item, name='remove_item'),
]