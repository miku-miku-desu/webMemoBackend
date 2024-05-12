import actor


class Sync:

    user: actor.User
    memo: actor.Memo
    username: str

    def __init__(self, username: str):
        self.username = username

    def verify(self, token: str, timestamp: int):
        try:
            self.user = actor.User.get(self.username)
        except ValueError as e:
            return False, "user not found"
        result = self.user.verify_login_token(token, timestamp)
        if result:
            try:
                self.memo = actor.Memo.get(self.username)
            except ValueError as e:
                self.memo = actor.Memo.create(self.username, "", 0)
            return True
        else:
            return False

    def toLocal(self):
        return self.memo

    def toRemote(self, memo_content: str, time: int):
        self.memo.update(memo_content, time)
        return True

    def auto_update(self, memo_content: str, time: int):
        if self.memo.update_time < time:
            return self.toRemote(memo_content, time)
        else:
            return self.toLocal()

