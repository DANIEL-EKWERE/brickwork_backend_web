from sqlalchemy import text





def construct_insert_sql(*, table_name: str, columns: list[str]) -> str:
    """
    Constructs an SQL INSERT statement for multiple entries with conflict handling.

    Parameters:
    - table_name (str): The name of the database table.
    - columns (list[str]): A list of column names for insertion.
    each representing values for a row corresponding to the columns.

    Returns:
    - str: A SQL query string for bulk inserting data with conflict handling.
    """
    # SQL base insert statement
    column_names = ", ".join(columns)
    placeholders = ", ".join([f":{column}" for column in columns])  # Using parameterized queries for safety

    sql = f"INSERT OR IGNORE INTO {table_name} ({column_names}) VALUES ({placeholders})"

    return text(sql)

