# from celery import shared_task, group
# from django.utils import timezone
# from .models import TaskHistory
# from src import ingestion
# import os

# import logging
# logger = logging.getLogger(__name__)


# LOG_DIR = "logs"
# os.makedirs(LOG_DIR, exist_ok=True)



# def create_task_entry(self, name):
#     return TaskHistory.objects.create(
#         task_id=self.request.id,
#         script_name=name,
#         status="STARTED",
#         start_time=timezone.now()
#     )

# def log_output(filename, message):
#     log_file = os.path.join(LOG_DIR, filename)
#     with open(log_file, "a") as f:
#         f.write(f"[{timezone.now()}] {message}\n")

# @shared_task(bind=True)
# def run_export_category(self):
#     entry = create_task_entry(self, "export_category_to_json")
#     try:
#         ingestion.export_category_to_json()
#         log_output("ingestion.log", "Export category completed successfully.")
#         entry.status = "SUCCESS"
#     except Exception as e:
#         log_output("ingestion.log", f"ERROR: {str(e)}")
#         entry.status = "FAILED"
#     finally:
#         entry.end_time = timezone.now()
#         entry.save()
#     return entry.status

# @shared_task(bind=True)
# def run_export_color(self):
#     logger.info("run_export_color called")
#     entry = create_task_entry(self, "export_color_to_json")
#     try:
#         ingestion.export_color_to_json()
#         log_output("ingestion.log", "Export color completed successfully.")
#         logger.info("Export color completed successfully.")
#         entry.status = "SUCCESS"
#     except Exception as e:
#         log_output("ingestion.log", f"ERROR: {str(e)}")
#         entry.status = "FAILED"
#         logger.error("Export color failed.")
#     finally:
#         entry.end_time = timezone.now()
#         entry.save()
#     return entry.status

# @shared_task(bind=True)
# def run_export_parts(self):
#     entry = create_task_entry(self, "export_parts_to_json")
#     try:
#         ingestion.export_parts_to_json()
#         log_output("ingestion.log", "Export parts completed successfully.")
#         entry.status = "SUCCESS"
#     except Exception as e:
#         log_output("ingestion.log", f"ERROR: {str(e)}")
#         entry.status = "FAILED"
#     finally:
#         entry.end_time = timezone.now()
#         entry.save()
#     return entry.status

# @shared_task(bind=True)
# def run_export_minifigures(self):
#     entry = create_task_entry(self, "export_minifigures_to_json")
#     try:
#         ingestion.export_minifigures_to_json()
#         log_output("ingestion.log", "Export minifigures completed successfully.")
#         log_output("ingestion.log", "Export color completed successfully.")
#         entry.status = "SUCCESS"
#     except Exception as e:
#         log_output("ingestion.log", f"ERROR: {str(e)}")
#         entry.status = "FAILED"
#     finally:
#         entry.end_time = timezone.now()
#         entry.save()
#     return entry.status

# @shared_task(bind=True)
# def run_export_gears(self):
#     entry = create_task_entry(self, "export_gears_to_json")
#     try:
#         ingestion.export_gears_to_json()
#         log_output("ingestion.log", "Export gears completed successfully.")
#         entry.status = "SUCCESS"
#     except Exception as e:
#         log_output("ingestion.log", f"ERROR: {str(e)}")
#         entry.status = "FAILED"
#     finally:
#         entry.end_time = timezone.now()
#         entry.save()
#     return entry.status

# @shared_task(bind=True)
# def run_export_parts_with_colors(self):
#     entry = create_task_entry(self, "export_parts_with_colors_to_json")
#     try:
#         ingestion.export_parts_with_colors_to_json()
#         log_output("ingestion.log", "Export parts with colors completed successfully.")
#         entry.status = "SUCCESS"
#     except Exception as e:
#         log_output("ingestion.log", f"ERROR: {str(e)}")
#         entry.status = "FAILED"
#     finally:
#         entry.end_time = timezone.now()
#         entry.save()
#     return entry.status

# # Repeat this pattern for parts, minifigures, gears, parts_with_colors

# @shared_task(bind=True)
# def run_all_exports(self):
#     entry = create_task_entry(self, "run_all_exports")
#     try:
#         ingestion.run_all_exports()
#         log_output("ingestion.log", "All exports completed successfully.")
#         entry.status = "SUCCESS"
#     except Exception as e:
#         log_output("ingestion.log", f"ERROR: {str(e)}")
#         entry.status = "FAILED"
#     finally:
#         entry.end_time = timezone.now()
#         entry.save()
#     return entry.status

# @shared_task(bind=True)
# def run_all_exports_parallel1(self):
#     """
#     Run each export as a separate Celery task in parallel.
#     """
#     entry = create_task_entry(self, "run_all_exports_parallel")
#     try:
#         jobs = group([
#             run_export_category.s(),
#             run_export_color.s(),
#             # add others: run_export_parts.s(), etc.
#         ])()
#         jobs.join()  # wait for all to finish
#         log_output("ingestion.log", "Parallel exports completed.")
#         entry.status = "SUCCESS"
#     except Exception as e:
#         log_output("ingestion.log", f"ERROR: {str(e)}")
#         entry.status = "FAILED"
#     finally:
#         entry.end_time = timezone.now()
#         entry.save()
#     return entry.status

# from celery import group

# @shared_task(bind=True)
# def run_all_exports_parallel(self):
#     """
#     Run all injection tasks in parallel
#     """
#     task_entry = TaskHistory.objects.create(
#         task_id=self.request.id,
#         script_name="run_all_exports_parallel",
#         status="STARTED",
#         start_time=timezone.now()
#     )

#     try:
#         # launch all 6 tasks in parallel
#         job = group(
#             run_export_category.s(),
#             run_export_color.s(),
#             run_export_parts.s(),
#             run_export_minifigures.s(),
#             run_export_gears.s(),
#             run_export_parts_with_colors.s()
#         )
#         job.apply_async()
#         log_output("ingestion.log", "Parallel exports completed.")
#         task_entry.status = "SUCCESS"
#     except Exception as e:
#         task_entry.status = "FAILED"
#     finally:
#         task_entry.end_time = timezone.now()
#         task_entry.save()
#     return task_entry.status


from celery import shared_task, group
from django.utils import timezone
from .models import TaskHistory
from src import ingestion
from src import downloader  # Add this import
import os
from django.conf import settings

import logging
logger = logging.getLogger(__name__)

# LOG_DIR = "logs"
# os.makedirs(LOG_DIR, exist_ok=True)
# Compute absolute project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def create_task_entry(self, name):
    return TaskHistory.objects.create(
        task_id=self.request.id,
        script_name=name,
        status="STARTED",
        start_time=timezone.now()
    )

def log_output(filename, message):
    print("Logging called")
    # log_file = os.path.join(LOG_DIR, filename)
    log_file = settings.LOG_FILE
    print(f"Logging to: {os.path.abspath(log_file)}")
    with open(log_file, "a") as f:
        f.write(f"[{timezone.now()}] {message}\n")
        print("message logged")

# NEW TASK: Download XML files from BrickLink
@shared_task(bind=True)
def run_initialise_data(self):
    """Download XML files from BrickLink"""
    entry = create_task_entry(self, "initialise_data")
    try:
        log_output("ingestion.log", "Starting BrickLink data initialisation...")
        ingestion.main()
        log_output("ingestion.log", "Initialisation completed successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("ingestion.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
        logger.error(f"Initialisation failed: {str(e)}")
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status


# NEW TASK: Download XML files from BrickLink
@shared_task(bind=True)
def run_download_data(self):
    """Download XML files from BrickLink"""
    entry = create_task_entry(self, "download_data")
    try:
        log_output("ingestion.log", "Starting BrickLink data download...")
        downloader.main()
        log_output("ingestion.log", "Download completed successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("ingestion.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
        logger.error(f"Download failed: {str(e)}")
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status

# NEW TASK: Full ingestion (XML → DB → S3)
@shared_task(bind=True)
def run_full_ingestion(self):
    """Import XML to database and export to S3"""
    entry = create_task_entry(self, "full_ingestion")
    try:
        log_output("ingestion.log", "Starting full ingestion pipeline...")
        ingestion.main()
        log_output("ingestion.log", "Full ingestion completed successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("ingestion.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
        logger.error(f"Ingestion failed: {str(e)}")
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status

@shared_task(bind=True)
def run_export_category(self):
    entry = create_task_entry(self, "export_category_to_json")
    try:
        log_output("ingestion.log", "Starting category export...")
        ingestion.export_category_to_json()
        log_output("ingestion.log", "Export category completed successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("ingestion.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status

@shared_task(bind=True)
def run_export_color(self):
    entry = create_task_entry(self, "export_color_to_json")
    try:
        log_output("ingestion.log", "Starting color export...")
        ingestion.export_color_to_json()
        log_output("ingestion.log", "Export color completed successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("ingestion.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status

@shared_task(bind=True)
def run_export_parts(self):
    entry = create_task_entry(self, "export_parts_to_json")
    try:
        log_output("ingestion.log", "Starting parts export...")
        ingestion.export_parts_to_json()
        log_output("ingestion.log", "Export parts completed successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("ingestion.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status

@shared_task(bind=True)
def run_export_minifigures(self):
    entry = create_task_entry(self, "export_minifigures_to_json")
    try:
        log_output("ingestion.log", "Starting minifigures export...")
        ingestion.export_minifigures_to_json()
        log_output("ingestion.log", "Export minifigures completed successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("ingestion.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status

@shared_task(bind=True)
def run_export_gears(self):
    entry = create_task_entry(self, "export_gears_to_json")
    try:
        log_output("ingestion.log", "Starting gears export...")
        ingestion.export_gears_to_json()
        log_output("ingestion.log", "Export gears completed successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("ingestion.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status

@shared_task(bind=True)
def run_export_parts_with_colors(self):
    entry = create_task_entry(self, "export_parts_with_colors_to_json")
    try:
        log_output("ingestion.log.log", "Starting parts with colors export...")
        ingestion.export_parts_with_colors_to_json()
        log_output("ingestion.log.log", "Export parts with colors completed successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("ingestion.log.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status

@shared_task(bind=True)
def run_all_exports(self):
    """Run all exports sequentially"""
    entry = create_task_entry(self, "run_all_exports")
    try:
        log_output("ingestion.log", "Starting all exports...")
        ingestion.run_all_exports()
        log_output("ingestion.log", "All exports completed successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("ingestion.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status

@shared_task(bind=True)
def run_all_exports_parallel(self):
    """Run all exports in parallel"""
    entry = create_task_entry(self, "run_all_exports_parallel")
    try:
        log_output("ingestion.log", "Starting parallel exports...")
        job = group(
            run_export_category.s(),
            run_export_color.s(),
            run_export_parts.s(),
            run_export_minifigures.s(),
            run_export_gears.s(),
            run_export_parts_with_colors.s()
        )
        job.apply_async()
        log_output("ingestion.log", "Parallel exports queued.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("ingestion.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status

# NEW: Complete pipeline task
@shared_task(bind=True)
def run_complete_pipeline(self):
    """Download → Import → Export (full pipeline)"""
    entry = create_task_entry(self, "complete_pipeline")
    try:
        log_output("ingestion.log", "Starting complete pipeline...")
        
        # Step 1: Download
        log_output("ingestion.log", "Step 1: Downloading data...")
        downloader.main()
        
        # Step 2: Import to DB and export to S3
        log_output("ingestion.log", "Step 2: Importing and exporting...")
        ingestion.main()
        
        log_output("ingestion.log", "Complete pipeline finished successfully.")
        entry.status = "SUCCESS"
    except Exception as e:
        log_output("ingestion.log", f"ERROR: {str(e)}")
        entry.status = "FAILED"
    finally:
        entry.end_time = timezone.now()
        entry.save()
    return entry.status
