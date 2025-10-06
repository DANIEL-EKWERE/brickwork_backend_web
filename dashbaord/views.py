from fileinput import filename
from django.shortcuts import render
# from django.http import JsonResponse
# from .tasks import run_script, run_all
# import os
# from celery.result import AsyncResult
# from django.http import HttpResponse
# from brickwork_backend.celery import app
# from .models import TaskHistory

# def task_history(request):
#     history = TaskHistory.objects.order_by("-start_time")[:20]  # latest 20
#     return render(request, "dashboard/history.html", {"history": history})


# def stop_task(request, task_id):
#     """Stop a running Celery task"""
#     res = AsyncResult(task_id, app=app)
#     res.revoke(terminate=True, signal="SIGKILL")  # force kill
#     return JsonResponse({"task_id": task_id, "status": "revoked"})




# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# LOG_DIR = os.path.join(BASE_DIR, "logs")

# def view_log(request, script_name):
#     """Show logs with auto-refresh + highlighting"""
#     log_file = os.path.join(LOG_DIR, f"{script_name}.log")

#     if not os.path.exists(log_file):
#         logs = ["No logs found."]
#     else:
#         with open(log_file, "r") as f:
#             logs = f.readlines()

#     return render(request, "dashboard/logs.html", {
#         "script_name": script_name,
#         "logs": logs,
#     })

def index(request):
    return render(request, "dashboard/index.html")

# def run_single_task(request, script_name):
#     task = run_script.delay(script_name)
#     return JsonResponse({"task_id": task.id, "status": "queued"})

# def run_all_tasks(request):
#     task = run_all.delay()
#     return JsonResponse({"task_id": task.id, "status": "queued"})

# def task_status(request, task_id):
#     from celery.result import AsyncResult
#     res = AsyncResult(task_id)
#     return JsonResponse({"task_id": task_id, "status": res.status})


# from . import tasks

# def run_task(request, task_name):
#     task_map = {
#         "category": tasks.run_export_category,
#         "color": tasks.run_export_color,
#         "parts": tasks.run_export_parts,
#         "minifigures": tasks.run_export_minifigures,
#         "gears": tasks.run_export_gears,
#         "parts_colors": tasks.run_export_parts_with_colors,
#         "all": tasks.run_all_exports,
#         "parallel": tasks.run_all_exports_parallel,
#     }
#     if task_name not in task_map:
#         return JsonResponse({"error": "Invalid task"}, status=400)

#     task = task_map[task_name].delay()
#     return JsonResponse({"task_id": task.id})

import os
from django.http import JsonResponse
from . import tasks
from django.http import JsonResponse

LOG_DIR = "logs"
LOG_FILE = "ingestion.log"


def run_task(request, task_name):
    task_map = {
    "download": tasks.run_download_data,  # NEW
    "ingestion": tasks.run_full_ingestion,  # NEW
    "pipeline": tasks.run_complete_pipeline,  # NEW (all-in-one)
    "category": tasks.run_export_category,
    "color": tasks.run_export_color,
    "parts": tasks.run_export_parts,
    "minifigures": tasks.run_export_minifigures,
    "gears": tasks.run_export_gears,
    "parts_colors": tasks.run_export_parts_with_colors,
    "all": tasks.run_all_exports,
    "parallel": tasks.run_all_exports_parallel,
    "initialise": tasks.run_initialise_data,  # NEW
    # "parallel1": tasks.run_all_exports_parallel1,
}
    if task_name not in task_map:
        return JsonResponse({"error": "Invalid task"}, status=400)

    task = task_map[task_name].delay()
    # global LOG_FILE
    # LOG_FILE= f"{task_name}.log"
    print(f"here ===> {LOG_FILE}")
    return JsonResponse({"task_id": task.id})



def get_logs(request):
    log_file = os.path.join(LOG_DIR, LOG_FILE)
    print(log_file)
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            content = f.read()
    else:
        content = "No logs available yet."
        print("No logs available yet.")
    return JsonResponse({"logs": content})

def response_data(request):
    return render(request, "dashboard/response.html")