from django.contrib.auth.decorators import login_required
from fileinput import filename
from django.shortcuts import render
from django.conf import settings
from .models import IngestionLog
from django.core.files.storage import FileSystemStorage
from .models import UploadedXML
import os
from . import tasks
from src import ingestion
from django.views.decorators.http import require_POST
from django.http import JsonResponse


@login_required(login_url='login')
def index(request):
    return render(request, "dashboard/index.html")





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



# Individual views for specific tasks (POST only)
@login_required(login_url='login')
@require_POST
def initialise_data_view(request):
    """Initialize data (calls ingestion.run_initialise_data)."""
    fn = getattr(ingestion, 'main', None)
    if not fn:
        return JsonResponse({'error': 'Not implemented'}, status=400)
    try:
        data = fn()  # run the export function directly
        return JsonResponse({'status': 'success', 'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='login')
@require_POST
def export_color_view(request):
    fn = getattr(ingestion, 'export_color_to_json', None)
    if not fn:
        return JsonResponse({'error': 'Not implemented'}, status=400)
    try:
        data = fn()  # run the export function directly
        return JsonResponse({'status': 'success', 'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='login')
# @require_POST
# def export_category_view(request):
#     fn = getattr(ingestion, 'export_category_to_json', None)
#     if not fn:
#         return JsonResponse({'error': 'Not implemented'}, status=400)
#     print(f"export category called===={fn}")
#     fn()
#     return JsonResponse({"task_id": "export_category_to_json"})


@login_required(login_url='login')
@require_POST
def export_category_view(request):
    print("exported category method called")
    fn = getattr(ingestion, 'export_category_to_json', None)
    if not fn:
        return JsonResponse({'error': 'Not implemented'}, status=400)

    try:
        data = fn()  # run the export function directly
        print(f"exported category data: {data}")
        return JsonResponse({'status': 'success', 'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='login')
@require_POST
def export_parts_view(request):
    fn = getattr(ingestion, 'export_parts_to_json', None)
    if not fn:
        return JsonResponse({'error': 'Not implemented'}, status=400)
    try:
        data = fn()  # run the export function directly
        return JsonResponse({'status': 'success', 'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='login')
@require_POST
def export_minifigures_view(request):
    fn = getattr(ingestion, 'export_minifigures_to_json', None)
    if not fn:
        return JsonResponse({'error': 'Not implemented'}, status=400)
    try:
        data = fn()  # run the export function directly
        return JsonResponse({'status': 'success', 'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='login')
@require_POST
def export_gears_view(request):
    fn = getattr(ingestion, 'export_gears_to_json', None)
    if not fn:
        return JsonResponse({'error': 'Not implemented'}, status=400)
    try:
        data = fn()  # run the export function directly
        return JsonResponse({'status': 'success', 'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='login')
@require_POST
def export_parts_with_colors_view(request):
    fn = getattr(ingestion, 'export_parts_with_colors_to_json', None)
    if not fn:
        return JsonResponse({'error': 'Not implemented'}, status=400)
    try:
        data = fn()  # run the export function directly
        return JsonResponse({'status': 'success', 'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='login')
@require_POST
def run_all_exports_view(request):
    fn = getattr(ingestion, 'run_all_exports', None)
    if not fn:
        return JsonResponse({'error': 'Not implemented'}, status=400)
    try:
        data = fn()  # run the export function directly
        return JsonResponse({'status': 'success', 'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='login')
@require_POST
def run_all_exports_parallel_view(request):
    fn = getattr(ingestion, 'run_all_exports_parallel', None)
    if not fn:
        return JsonResponse({'error': 'Not implemented'}, status=400)
    try:
        data = fn()  # run the export function directly

        return JsonResponse({'status': 'success', 'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def home(request):
    return render(request, "dashboard/Features.html")

def pricing(request):
    return render(request, "dashboard/Pricing.html")

def blog(request):
    return render(request, "dashboard/Blog.html")



@login_required(login_url='login')
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

@csrf_exempt  
@require_http_methods(["POST", "DELETE"])  
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



@login_required(login_url='login')
def upload_xml_page(request):
    """Render the upload XML page."""
    return render(request, "dashboard/upload_xml.html")

@csrf_exempt
def upload_xml(request):
    """Handle XML file upload."""
    if request.method == "POST" and request.FILES.get("xml_file"):
        xml_file = request.FILES["xml_file"]
        if not xml_file.name.lower().endswith(".xml"):
            return JsonResponse({"error": "Only .xml files are allowed."}, status=400)
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, ""))
        filename = fs.save(xml_file.name, xml_file)
        UploadedXML.objects.create(file=f"{filename}")
        return JsonResponse({"message": f"{xml_file.name} uploaded successfully!"})
    return JsonResponse({"error": "No file uploaded."}, status=400)



# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
from django.db import connections




# Map of your actual tables and their primary keys
TABLE_PRIMARY_KEYS = {
    'parts': 'item_id',
    'parts_with_colors': 'sn',
    'sets': 'item_id',
    'inventory': 'inventory_id',
    'category': 'id',
    'color': 'id',
    'minifigures': 'item_id',
    'gears': 'item_id',
}

allowed_tables = ['parts', 'parts_with_colors', 'sets', 'inventory', 'category', 'color', 'minifigures', 'gears']
#with connections['brick_works'].cursor() as cursor:


def get_primary_key_column(table_name):
    """Get the primary key column name for a table"""
    return TABLE_PRIMARY_KEYS.get(table_name, 'id')



def get_table_data(request, table_name):
    """Get all data from a table"""

    allowed_tables = ['parts', 'parts_with_colors', 'sets', 'inventory', 'category', 'color', 'minifigures', 'gears']

    if table_name not in allowed_tables:
        return JsonResponse({'error': 'Table not allowed'}, status=400)
    
    try:
        with connections['brick_works'].cursor() as cursor:
            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]

            # Get primary key
            primary_key = get_primary_key_column(table_name)
            
            # Get data
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            # Convert to list of dicts
            data = []
            for row in rows:
                data.append(dict(zip(columns, row)))
            
            return JsonResponse({
                'columns': columns,
                'rows': data,
                'count': len(data),
                'primary_key': primary_key
            })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def update_row(request, table_name, row_id):
    if request.method != 'PUT':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    if table_name not in TABLE_PRIMARY_KEYS:
        return JsonResponse({'error': 'Table not allowed'}, status=400)

    try:
        data = json.loads(request.body)
        primary_key = get_primary_key_column(table_name)

        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        values = list(data.values())
        values.append(row_id)

        with connections['brick_works'].cursor() as cursor:
            query = f"UPDATE {table_name} SET {set_clause} WHERE {primary_key} = ?"
            print(f"Running query: {query} with {values}")
            cursor.execute(query, values)
            connections['brick_works'].commit()

            if cursor.rowcount == 0:
                return JsonResponse({'error': 'Row not found'}, status=404)

        return JsonResponse({'status': 'success', 'message': 'Row updated'})

    except Exception as e:
         import traceback
         print("❌ ERROR DURING UPDATE:")
         traceback.print_exc()
         return JsonResponse({'error': str(e)}, status=500)



@csrf_exempt
def delete_row(request, table_name, row_id):
    print("calling method====")
    print(f"table name {table_name}, row id {row_id}")
    """Delete a specific row"""
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if table_name not in TABLE_PRIMARY_KEYS:
            return JsonResponse({'error': 'Table not allowed'}, status=400)
    
    try:
        primary_key = get_primary_key_column(table_name)

        with connections['brick_works'].cursor() as cursor:
            cursor.execute(f"DELETE FROM {table_name} WHERE {primary_key} = ?", [row_id])
        
        return JsonResponse({'status': 'success', 'message': 'Row deleted'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def add_row(request, table_name):
    """Add a new row"""
    print("calling method====")
    print(f"table name ==== {table_name}")
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    allowed_tables = ['categories', 'color', 'parts', 'minifigures', 'gears', 'parts_colors']
    if table_name not in allowed_tables:
        return JsonResponse({'error': 'Table not allowed'}, status=400)
    
    try:
        data = json.loads(request.body)
        
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = list(data.values())

        with connections['brick_works'].cursor() as cursor:
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, values)
            connections['brick_works'].commit()  
            print("✅ Insert succeeded and committed")

            # Get the ID of the inserted row
            primary_key = get_primary_key_column(table_name)
            if primary_key == 'id' or primary_key.endswith('_id'):
                cursor.execute(f"SELECT last_insert_rowid()")
                new_id = cursor.fetchone()[0]
            else:
                new_id = data.get(primary_key)
        
        return JsonResponse({'status': 'success', 'message': 'Row added'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def db_viewer_page(request):
    # """Render the database viewer page"""
    # from django.shortcuts import render
    return render(request, 'dashboard/db-viewer.html')