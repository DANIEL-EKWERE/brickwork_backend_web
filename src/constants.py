from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

BASE_DIR = ROOT_DIR / "src"

COOKIES_FILE_NAME = "cookies.json"

DB_FILE_NAME = "brick_works.db"

LAST_RUN_FILE_NAME = "last_run_at.json"

LOGIN_URL = "https://www.bricklink.com/v2/login.page"

# BRICKLINK_EMAIL = "le_meridian"
BRICKLINK_EMAIL = "sofrosyninc@gmail.com"

BRICKLINK_PASSWORD = "Metallicoxide@5"
# BRICKLINK_PASSWORD = "test12345"

DOWNLOAD_PARTS_CSV = "https://www.bricklink.com/catalogDownload.asp?a=a&viewType=0&downloadType=T&itemType=P"

DOWNLOAD_PARTS_XML = "https://www.bricklink.com/catalogDownload.asp?a=a&viewType=0&itemType=P&selItemColor=Y&selWeight=Y&selYear=Y&downloadType=X"  # noqa E501

DOWNLOAD_COLORS_XML = "https://www.bricklink.com/catalogDownload.asp?a=a&viewType=3&downloadType=X"

DOWNLOAD_PARTS_WITH_COLORS_XML = "https://www.bricklink.com/catalogDownload.asp?a=a&viewType=5&downloadType=X"

DOWNLOAD_CATEGORY_XML = "https://www.bricklink.com/catalogDownload.asp?a=a&viewType=2&downloadType=X"

DOWNLOAD_ITEM_TYPES_XML = "https://www.bricklink.com/catalogDownload.asp?a=a&viewType=1&downloadType=X"

DOWNLOAD_MINIFIGURES_XML = "https://www.bricklink.com/catalogDownload.asp?a=a&viewType=0&itemType=M&selItemColor=Y&selWeight=Y&selYear=Y&downloadType=X"  # noqa E501

DOWNLOAD_GEARS_XML = "https://www.bricklink.com/catalogDownload.asp?a=a&viewType=0&itemType=G&selItemColor=Y&selWeight=Y&selYear=Y&downloadType=X"  # noqa E501

DOWNLOAD_SET_XML = "https://www.bricklink.com/catalogDownload.asp?a=a&viewType=0&itemType=S&selItemColor=Y&selWeight=Y&selYear=Y&downloadType=X" # noqa E501

LINKS_TO_DOWNLOAD = [
    (DOWNLOAD_CATEGORY_XML, "categories.xml"),
    (DOWNLOAD_COLORS_XML, "colors.xml"),
    (DOWNLOAD_ITEM_TYPES_XML, "itemtypes.xml"),
    (DOWNLOAD_PARTS_XML, "Parts.xml"),
    (DOWNLOAD_PARTS_WITH_COLORS_XML, "codes.xml"),
    (DOWNLOAD_MINIFIGURES_XML, "Minifigures.xml"),
    (DOWNLOAD_GEARS_XML, "Gear.xml"),
    (DOWNLOAD_SET_XML, "Sets.xml"),
]
