from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.index, name="dashboard"),
    # path("run/<str:script_name>/", views.run_single_task, name="run_script"),
    # path("run_all/", views.run_all_tasks, name="run_all"),
    # path("status/<str:task_id>/", views.task_status, name="task_status"),
    # path("logs/<str:script_name>/", views.view_log, name="view_log"),
    # path("history/", views.task_history, name="task_history"),

    # path("stop/<str:task_id>/", views.stop_task, name="stop_task"),  # 👈 NEW


    path("dashboard/run/<str:task_name>/", views.run_task, name="run_task"),
    path("dashboard/logs/", views.get_logs, name="get_logs"),
    path("dashboard/response/", views.response_data, name="response"),
    path("dashboard/clear-logs/", views.clear_log, name="clear_logs"),  # 👈 NEW
]

