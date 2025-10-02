import html
import json
from pprint import pprint
import threading
import urllib.request

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from common import upload_object_to_s3
from constants import LINKS_TO_DOWNLOAD, ROOT_DIR
from crud_util import construct_insert_sql
from database import Base, SessionLocal, engine
from schema import (
    Category,
    Codes,
    Color,
    Gears,
    Inventory,
    MiniFigures,
    Parts
)

# A lock object to manage database writes
db_write_lock = threading.Lock()
Base.metadata.create_all(bind=engine)

# """
# TODO:
# 1. Write data asynchronously
# 2. Push notification to mobile app on new updates to the database
# 3. Fail safe logic
# 4. Push data to aws bucket
# """

Inventory =  {}

def restore_from_backup(backup_file_path):
    if backup_file_path.exists():
        original_file_path = backup_file_path.with_suffix("")
        if original_file_path.exists():
            print(f"Cannot restore because the original file already exists: {original_file_path}")
        else:
            # Rename the backup file to the original file name
            backup_file_path.rename(original_file_path)
            print(f"Backup restored: {original_file_path}")
    else:
        print("Backup file does not exist, cannot restore.")


def get_db() -> Session:
    db = SessionLocal()
    try:
        return db  # Return the session directly
    finally:
        db.close()


def insert_xml_file_to_db(*, path, klass, columns_mapping):
    print(f"########## Start -> Write {klass.__tablename__} to Database ###########\n\n")
    df = pd.read_xml(path)[columns_mapping.keys()]
    df = df.rename(columns=columns_mapping).replace({np.nan: None})
    objs = df.to_dict("records")
    insert_to_db(klass=klass, columns=df.columns.values, params=objs)
    print(f"########## Completed {klass.__tablename__} write {len(objs)} items ###########\n\n")


def insert_to_db(*, klass, columns, params):
    if isinstance(params, list) and len(params) == 0:
        return

    db = get_db()
    sql = construct_insert_sql(table_name=klass.__tablename__, columns=columns)
    db.execute(sql, params=params)
    db.commit()


def get_known_colors(part_number, part_name, category_id):
    objs = []
    try:
        req = urllib.request.Request(
            f"https://www.bricklink.com/v2/catalog/catalogitem.page?P={part_number}#T=C",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, "html.parser")

        # Find the table containing color information
        # color_table = soup.find("div", {"class": "pciSelectColorDropdownList"})
        # known_colors = color_table.find_all("div", {"class": "pciSelectColorColorItem"})
        # Find all elements with data-tab='Known'
        known_items = soup.find_all("div", {"data-tab": "Known"})
        # Loop through each known item and print the desired values
        for item in known_items:
            objs.append(
                {
                    "item_id": part_number,
                    "item_name": part_name,
                    "category_id": category_id,
                    "color_name": item["data-name"],
                    "color_id": item["data-color"],
                    "color_code": item["data-rgb"],
                }
            )
    except AttributeError:
        print("Can't find known color try again")
    finally:
        return objs

def export_inventory_to_json():
    """Export file to aws console"""
    # TODO: upload the json file to s3 Bucket, give it a fixed URL
    db = get_db()
    list_of_data = []
    inventories = db.query(Inventory).all()
    print("%s inventories" % (len(inventories)))
    for inv in inventories:
        data = {
            "id": inv.inventory_id,
            "part_name": inv.item_name,
            "part_number": inv.item_id,
            "category_name": inv.category_name,
            "category_id": inv.category_id,
            "color_name": inv.color_name,
            "color_code": inv.color_code,
            "color_id": inv.color_id,
            "color_type": inv.color_type,
        }
        list_of_data.append(data)
    upload_object_to_s3(object=json.dumps(list_of_data), s3_file_name="inventory.json")


def export_minifigures_to_json():
    """Export Minifigure file to aws s3 bucket"""
    print("########## Start -> Exporting Minifigures to Json  ###########\n\n")

    db = get_db()
    list_of_data = []
    minifigures = db.query(
        MiniFigures.item_id, MiniFigures.name, MiniFigures.category,Category.category_name
        ).join(Category, MiniFigures.category == Category.category_id).all()
    print("%s mini figures" % (len(minifigures)))
    for minifig in minifigures:
        data = {
            "item_name": html.unescape(minifig.name),
            "item_id": minifig.item_id,
            "category_id": minifig.category,
            "category_name": html.unescape(minifig.category_name),
        }
        list_of_data.append(data)
    pprint(list_of_data[:5])
    upload_object_to_s3(object=json.dumps(list_of_data), s3_file_name="minifigures.json")
    print("%s Completed -> Minifigures Exported \n\n" % (len(minifigures)))

def export_gears_to_json():
    """Export Gears file to aws s3 bucket"""
    print("########## Start -> Exporting Gears to Json  ###########\n\n")
    db = get_db()
    list_of_data = []
    gears = db.query(
        Gears.item_id, Gears.name, Gears.category,Category.category_name
        ).join(Category, Gears.category == Category.category_id).all()
    print("%s gears" % (len(gears)))
    for gear in gears:
        data = {
            "item_id": gear.item_id,
            "item_name": html.unescape(gear.name),
            "category_id": gear.category,
            "category_name": html.unescape(gear.category_name),
        }
        list_of_data.append(data)
    pprint(list_of_data[:5])
    upload_object_to_s3(object=json.dumps(list_of_data), s3_file_name="gears.json")
    print("%s Completed -> Gears Exported \n\n" % (len(gears)),"\n")


def export_category_to_json():
    """Export Category file to aws s3 bucket"""
    print("########## Start -> Exporting Category to Json  ###########\n\n")
    db = get_db()
    list_of_data = []
    categories = db.query(Category).all()
    print("%s categories" % (len(categories)))
    for category in categories:
        data = {
            "category_id": category.category_id,
            "category_name": html.unescape(category.category_name),
        }
        list_of_data.append(data)
    pprint(list_of_data[:5])
    upload_object_to_s3(object=json.dumps(list_of_data), s3_file_name="categories.json")
    print("%s Completed -> Category Exported\n\n" % (len(categories)))

def export_color_to_json():
    """Export Color file to aws s3 bucket"""
    print("########## Start -> Exporting Color to Json  ###########\n\n")
    db = get_db()
    list_of_data = []
    colors = db.query(Color).all()
    print("%s colors" % (len(colors)))
    for color in colors:
        data = {
            "color_id": color.color_id,
            "color_name": html.unescape(color.color_name),
            "color_code": color.color_code,
            "color_type": color.color_type,
        }
        list_of_data.append(data)
    pprint(list_of_data[:5])
    upload_object_to_s3(object=json.dumps(list_of_data), s3_file_name="colors.json")
    print("%s Completed -> Color Exported\n\n" % (len(colors)))

def export_parts_to_json():
    """Export Parts file to aws s3 bucket"""
    print("########## Start -> Exporting Parts to Json  ###########\n\n")
    db = get_db()
    list_of_data = []
    parts = db.query(Parts.name,Parts.item_id,Parts.category, Category.category_name
                     ).join(Category,Parts.category == Category.category_id).all()
    print("%s parts" % (len(parts)))
    for part in parts:
        data = {
            "item_id": part.item_id,
            "name": html.unescape(part.name),
            "category_id": part.category,
            "category_name": html.unescape(part.category_name),
        }
        list_of_data.append(data)
    pprint(list_of_data[:5])
    upload_object_to_s3(object=json.dumps(list_of_data), s3_file_name="parts.json")
    print("%s Completed -> Parts Exported\n\n" % (len(parts)))

def export_parts_with_colors_to_json():

    db = get_db()
    list_of_data = []
    parts_with_colors = db.query(
        Codes.item_id, Codes.item_type, Codes.color_name, Color.color_id, Color.color_code, Color.color_type
    ).join(Color, Codes.color_name == Color.color_name).all()

    print("%s parts with colors" % (len(parts_with_colors)))
    for part in parts_with_colors:
        data = {
            "item_id": part.item_id,
            "color_name": html.unescape(part.color_name),
            "color_id": part.color_id,
            "color_code": part.color_code,
            "color_type": part.color_type,
        }
        list_of_data.append(data)
    pprint(list_of_data[:5])
    upload_object_to_s3(object=json.dumps(list_of_data), s3_file_name="parts_with_colors.json")
    print("%s Completed -> Parts with colors \n\n" % (len(parts_with_colors)))


def main():
    # TODO: Update these function to run in different sequence to improve speed
    """TODO:
    Run the following functions in parallel
    write_color_xml_to_database()
    write_category_xml_to_database()
    write_parts_xml_to_database()

    Run the following functions in series: each function is dependant on the preceding one

    write_missing_items()
    write_missing_items_to_inventory()
    update_color_in_inventory()
    update_parts_name_and_category_id_in_inventory()
    update_category_name_in_inventory()
    export_inventory_to_json()

    """
    for _, filename in LINKS_TO_DOWNLOAD:
        restore_from_backup(ROOT_DIR / "data" / (filename + ".bak"))

    insert_xml_file_to_db(
        path=(ROOT_DIR / "data" / "colors.xml"),
        klass=Color,
        columns_mapping={
            "COLOR": "color_id",
            "COLORNAME": "color_name",
            "COLORRGB": "color_code",
            "COLORTYPE": "color_type",
        },
    )
    insert_xml_file_to_db(
        path=(ROOT_DIR / "data" / "categories.xml"),
        klass=Category,
        columns_mapping={
            "CATEGORY": "category_id",
            "CATEGORYNAME": "category_name",
        },
    )

    insert_xml_file_to_db(
        path=(ROOT_DIR / "data" / "Parts.xml"),
        klass=Parts,
        columns_mapping={
            "ITEMID": "item_id",
            "ITEMNAME": "name",
            "CATEGORY": "category",
        },
    )



    insert_xml_file_to_db(
        path=(ROOT_DIR / "data" / "codes.xml"),
        klass=Codes,
        columns_mapping={
            "ITEMID": "item_id",
            "COLOR": "color_name",
            "ITEMTYPE": "item_type",
        },
    )

    insert_xml_file_to_db(
        path=(ROOT_DIR / "data" / "Minifigures.xml"),
        klass=MiniFigures,
        columns_mapping={
            "ITEMID": "item_id",
            "ITEMNAME": "name",
            "CATEGORY": "category",
        },
    )

    insert_xml_file_to_db(
        path=(ROOT_DIR / "data" / "Gear.xml"),
        klass=Gears,
        columns_mapping={
            "ITEMID": "item_id",
            "ITEMNAME": "name",
            "CATEGORY": "category",
        },
    )

    #### Upload to AWS S3 functions

    export_color_to_json()

    export_category_to_json()

    export_minifigures_to_json()


def run_all_exports():
    export_category_to_json()
    export_color_to_json()
    export_parts_to_json()
    export_minifigures_to_json()
    export_gears_to_json()
    export_parts_with_colors_to_json()

if __name__ == "__main__":
    run_all_exports()


'''
if __name__ == "__main__":
    # print("ingestion(): Running ingestion service manually...")
    # main()
    # print("ingestion(): Ingestion service completed.")
    # print("ingestion(): Running Export Minifigure manually...")
    # export_minifigures_to_json()
    export_category_to_json()
    export_color_to_json()
    export_parts_to_json()
    export_minifigures_to_json()
    export_gears_to_json()
    export_parts_with_colors_to_json()
'''