""" Defines the database tables and columns"""

from sqlalchemy import Column, Integer, String

from database import Base


class Parts(Base):
    __tablename__ = "parts"
    item_id = Column(String, primary_key=True)
    name = Column(String)
    category = Column(String)

class Codes(Base):
    __tablename__ = "parts_with_colors"
    sn = Column(Integer, primary_key=True)
    item_id = Column(String)
    color_name = Column(String)
    item_type = Column(String)


# class MissingParts(Base):
#     __tablename__ = "missing_parts"
#     item_id = Column(String, primary_key=True)
#     name = Column(String)
#     category = Column(String)

class Sets(Base):
    __tablename__ = "sets"
    item_id = Column(String, primary_key=True)
    name = Column(String)
    category = Column(String)

class Inventory(Base):
    __tablename__ = "inventory"
    inventory_id = Column(Integer, primary_key=True)
    item_id = Column(String)
    item_name = Column(String)
    category_id = Column(String)
    category_name = Column(String)
    color_id = Column(String)
    color_name = Column(String)
    color_code = Column(String)
    color_type = Column(String)


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    category_name = Column(String)
    category_id = Column(String)


class Color(Base):
    __tablename__ = "color"
    id = Column(Integer, primary_key=True)
    color_name = Column(String)
    color_id = Column(String)
    color_type = Column(String)
    color_code = Column(String)


class MiniFigures(Base):
    __tablename__ = "minifigures"
    item_id = Column(String, primary_key=True)
    name = Column(String)
    category = Column(String)


class Gears(Base):
    __tablename__ = "gears"
    item_id = Column(String, primary_key=True)
    name = Column(String)
    category = Column(String)


# class MissingMiniFigures(Base):
#     __tablename__ = "missing_minifigures"
#     item_id = Column(String, primary_key=True)
#     name = Column(String)
#     category = Column(String)


# class MissingGears(Base):
#     __tablename__ = "missing_gears"
#     item_id = Column(String, primary_key=True)
#     name = Column(String)
#     category = Column(String)
