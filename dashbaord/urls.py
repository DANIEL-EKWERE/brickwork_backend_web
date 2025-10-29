from django.urls import path
from . import views
from . import auth_view

urlpatterns = [
    path("dashboard/", views.index, name="dashboard"),
    # path("run/<str:script_name>/", views.run_single_task, name="run_script"),
    # path("run_all/", views.run_all_tasks, name="run_all"),
    # path("status/<str:task_id>/", views.task_status, name="task_status"),
    # path("logs/<str:script_name>/", views.view_log, name="view_log"),
    # path("history/", views.task_history, name="task_history"),

    # path("stop/<str:task_id>/", views.stop_task, name="stop_task"),  # 👈 NEW

    path("auth/login/", auth_view.login_view, name="login"),
    path("auth/signup/", auth_view.signup_view, name="signup"),
    path("logout/", auth_view.logout_view, name="logout"),
    path("", views.home, name="home"),
    path("dashboard/run/<str:task_name>/", views.run_task, name="run_task"),
    path("dashboard/logs/", views.get_logs, name="get_logs"),
    path("dashboard/response/", views.response_data, name="response"),
    path("dashboard/clear-logs/", views.clear_log, name="clear_logs"),  # 👈 NEW
    path("dashboard/upload-xml/", views.upload_xml_page, name="upload_xml_page"),
    path("dashboard/upload-xml/submit/", views.upload_xml, name="upload_xml"),
   
    path('dashboard/db-viewer/', views.db_viewer_page, name='db_viewer'),
    path('api/db/table/<str:table_name>/', views.get_table_data),
    path('api/db/table/<str:table_name>/row/<str:row_id>/', views.update_row),
    path('api/db/table/delete/<str:table_name>/row/<str:row_id>/', views.delete_row),
    path('api/db/table/add/<str:table_name>/', views.add_row),
    # Synchronous task endpoints (POST)
    path('dashboard/initialise/', views.initialise_data_view, name='initialise_data'),
    path('dashboard/export/color/', views.export_color_view, name='export_color'),
    path('dashboard/export/category/', views.export_category_view, name='export_category'),
    path('dashboard/export/parts/', views.export_parts_view, name='export_parts'),
    path('dashboard/export/minifigures/', views.export_minifigures_view, name='export_minifigures'),
    path('dashboard/export/gears/', views.export_gears_view, name='export_gears'),
    path('dashboard/export/parts_colors/', views.export_parts_with_colors_view, name='export_parts_with_colors'),
    path('dashboard/export/all/', views.run_all_exports_view, name='run_all_exports'),
    path('dashboard/export/all-parallel/', views.run_all_exports_parallel_view, name='run_all_exports_parallel'),
    path("dashboard/pricing/", views.pricing, name="pricing"),
    path("dashboard/blog/", views.blog, name="blog"),


]

