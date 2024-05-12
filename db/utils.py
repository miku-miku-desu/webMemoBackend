import mysql.connector
from contextlib import contextmanager
from typing import Dict, List, Tuple
from config import default_database
import logging


logger = logging.getLogger(__name__)


# accept Dict as the first argument containing database information or kwargs containing database information
# a transaction
@contextmanager
def connect(*args, **kwargs):
    if args:
        assert isinstance(args[0], Dict)
        db_info = args[0]
    elif kwargs:
        db_info = kwargs
    else:
        raise ValueError("No database information provided")

    db_info["autocommit"] = False
    db_info["charset"] = "utf8mb4"
    db_info["collation"] = "utf8mb4_unicode_ci"
    if "use_database" not in kwargs:
        db_info["database"] = default_database
    conn = mysql.connector.connect(**db_info)
    try:
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()