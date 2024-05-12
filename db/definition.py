from config import default_database
from .utils import connect
import logging


logger = logging.getLogger(__name__)


def user_definition(*args, **kwargs):
    logger.info("init user table")
    with connect(*args, **kwargs) as cursor:
        cursor.execute("""
            create table if not exists user (
                username varchar(20) primary key not null,
                password varchar(255) not null,
                salt varchar(255) not null
            )
        """)    # salt本应存到另一个库中


def memo_definition(*args, **kwargs):
    logger.info("init memo table")
    with connect(*args, **kwargs) as cursor:
        cursor.execute("""
            create table if not exists memo (
                username varchar(20) primary key not null,
                content text,
                update_time bigint,
                foreign key (username) references user(username)
            )
        """)


def init_database(*args, **kwargs):
    logger.info("init database memo")
    with connect(use_database = False, *args, **kwargs) as cursor:
        cursor.execute(f"create database if not exists {default_database}")


def init_db(*args, **kwargs):
    init_database(*args, **kwargs)
    user_definition(*args, **kwargs)
    memo_definition(*args, **kwargs)