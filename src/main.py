from db_connection import TargetDB, MainDB
from db_schema import DBSchema
from schema_compare import SchemaCompare
from migration import Migration

target_db = TargetDB()  # Образец
main_db = MainDB()  # Боевая

target_schema = DBSchema(target_db.conn).get_tables()
main_schema = DBSchema(main_db.conn).get_tables()

changes = SchemaCompare(target_schema, main_schema).difference()

Migration(changes).apply(main_db.conn)
