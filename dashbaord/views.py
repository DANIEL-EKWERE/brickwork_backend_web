from fileinput import filename
from django.shortcuts import render
from django.conf import settings
from .models import IngestionLog

def index(request):
    return render(request, "dashboard/index.html")



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

def home(request):
    return render(request, "dashboard/home.html")




def get_logs(request):
    logs = IngestionLog.objects.order_by('-created_at')[:500]
    print
    content = "\n".join(reversed([log.message for log in logs]))
    return JsonResponse({"logs": content or "No logs available yet."})


def response_data(request):
    return render(request, "dashboard/response.html")

#@require_POST
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt  # Remove this if you're handling CSRF tokens properly
@require_http_methods(["POST", "DELETE"])  # Only allow POST/DELETE, not GET
def clear_log(request):
    try:
        count, _ = IngestionLog.objects.all().delete()
        return JsonResponse({
            "status": "success",
            "message": f"Cleared {count} log entries."
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })

