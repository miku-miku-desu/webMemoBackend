import random
from db.utils import connect
import utils
from config import get_config


class User:

    __username: str
    __passwd: str
    __salt: str

    @property
    def username(self):
        return self.__username

    @property
    def passwd(self):
        return self.__passwd

    @property
    def salt(self):
        return self.__salt

    def __init__(self):
        self.__username = ""
        self.__passwd = ""
        self.__salt = ""

    def save(self):
        with connect(get_config()) as cursor:
            cursor.execute("""
                update user
                set password = %s, salt = %s
                where username = %s
                """, (self.__passwd, self.__salt, self.__username)
            )

    def add(self):
        with connect(get_config()) as cursor:
            cursor.execute("""
                insert into user (username, password, salt)
                values (%s, %s, %s)
            """, (self.__username, self.__passwd, self.__salt))

    def get_login_token(self):
        timestamp = utils.get_timestamp()
        return utils.sha256(self.__username + self.passwd + str(timestamp)), timestamp

    def verify_login_token(self, token: str, timestamp: int):
        return token == utils.sha256(self.__username + self.passwd + str(timestamp))

    def verify_passwd(self, passwd: str):
        return self.__passwd == utils.sha256(passwd + self.__salt)

    def update_passwd(self, passwd: str):
        self.__passwd = utils.sha256(passwd + self.__salt)
        self.save()

    @classmethod
    def create(cls, username: str, passwd: str):
        user = cls()
        user.__username = username
        user.__salt = utils.number_sha256(random.randint(10000000, 99999999))
        user.__passwd = utils.sha256(passwd + user.__salt)
        user.add()

        return user

    @classmethod
    def get(cls, username: str):
        user = cls()
        with connect(get_config()) as cursor:
            cursor.execute("""
                select username, password, salt
                from user
                where username = %s
            """, (username,))
            result = cursor.fetchone()
            if result:
                user.__username, user.__passwd, user.__salt = result
            else:
                raise ValueError("user not found")

        return user


class Memo:
    __username: str
    __content: str
    __update_time: int

    @property
    def username(self):
        return self.__username

    @property
    def content(self):
        return self.__content

    @property
    def update_time(self):
        return self.__update_time

    def __init__(self):
        self.__username = ""
        self.__content = ""
        self.__update_time = 0

    def update(self, memo: str, update_time: int):
        self.__content = memo
        self.__update_time = update_time
        with connect(get_config()) as cursor:
            cursor.execute("""
                update memo
                set content = %s, update_time = %s
                where username = %s
            """, (self.__content, self.__update_time, self.__username))

    def add(self):
        with connect(get_config()) as cursor:
            cursor.execute("""
                insert into memo (username, content, update_time)
                values (%s, %s, %s)
            """, (self.__username, self.__content, self.__update_time))

    @classmethod
    def create(cls, username: str, memo: str, update_time: int):
        memo_obj = cls()
        memo_obj.__username = username
        memo_obj.__content = memo
        memo_obj.__update_time = update_time
        memo_obj.add()

        return memo

    @classmethod
    def get(cls, username: str):
        memo_obj = cls()
        with connect(get_config()) as cursor:
            cursor.execute("""
                select username, content, update_time
                from memo
                where username = %s
            """, (username,))
            result = cursor.fetchone()
            if result:
                memo_obj.__username, memo_obj.__content, memo_obj.__update_time = result
            else:
                raise ValueError("memo not found")

        return memo_obj
