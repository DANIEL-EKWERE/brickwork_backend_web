from celery import shared_task, group
from django.utils import timezone
from .models import TaskHistory
import ingestion
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def create_task_entry(self, name):
    return TaskHistory.objects.create(
        task_id=self.request.id,
        script_name=name,
        status="STARTED",
        start_time=timezone.now()
    )

def log_output(filename, message):
    log_file = os.path.join(LOG_DIR, filename)
    with open(log_file, "a") as f:
        f.write(f"[{timezone.now()}] {message}\n")

@shared_task(bind=True)
def run_export_category(self):
    entry = create_task_entry(self, "export_category_to_json")
    try:
        ingestion.export_category_to_json()
        log_output("category.log", "Export category completed successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("category.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status

@shared_task(bind=True)
def run_export_color(self):
    entry = create_task_entry(self, "export_color_to_json")
    try:
        ingestion.export_color_to_json()
        log_output("color.log", "Export color completed successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("color.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status

@shared_task(bind=True)
def run_export_parts(self):
    entry = create_task_entry(self, "export_parts_to_json")
    try:
        ingestion.export_parts_to_json()
        log_output("parts.log", "Export parts completed successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("parts.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status

@shared_task(bind=True)
def run_export_minifigures(self):
    entry = create_task_entry(self, "export_minifigures_to_json")
    try:
        ingestion.export_minifigures_to_json()
        log_output("minifigures.log", "Export minifigures completed successfully.")
        log_output("color.log", "Export color completed successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("color.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status

@shared_task(bind=True)
def run_export_gears(self):
    entry = create_task_entry(self, "export_gears_to_json")
    try:
        ingestion.export_gears_to_json()
        log_output("gears.log", "Export gears completed successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("gears.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status

@shared_task(bind=True)
def run_export_parts_with_colors(self):
    entry = create_task_entry(self, "export_parts_with_colors_to_json")
    try:
        ingestion.export_parts_with_colors_to_json()
        log_output("parts_colors.log", "Export parts with colors completed successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("parts_colors.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status

# Repeat this pattern for parts, minifigures, gears, parts_with_colors

@shared_task(bind=True)
def run_all_exports(self):
    entry = create_task_entry(self, "run_all_exports")
    try:
        ingestion.run_all_exports()
        log_output("all.log", "All exports completed successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("all.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status

@shared_task(bind=True)
def run_all_exports_parallel(self):
    """
    Run each export as a separate Celery task in parallel.
    """
    entry = create_task_entry(self, "run_all_exports_parallel")
    try:
        jobs = group([
            run_export_category.s(),
            run_export_color.s(),
            # add others: run_export_parts.s(), etc.
        ])()
        jobs.join()  # wait for all to finish
        log_output("parallel.log", "Parallel exports completed.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("parallel.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status
