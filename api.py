from config import get_endpoint, get_can_register, load_config
import actor
import flask
from flask_cors import CORS
import sync
import logging


logging.basicConfig(level = logging.INFO, format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s")


load_config()
api = flask.Flask(__name__)
CORS(api)


@api.route(get_endpoint() + "user/login", methods=["POST"])
def login():
    try:
        username = flask.request.json["username"]
        passwd = flask.request.json["passwd"]
    except KeyError as e:
        return flask.jsonify({"status": False, "message": "error request"}), 400
    try:
        user = actor.User.get(username)
    except ValueError as e:
        return flask.jsonify({"status": False, "message": "username or passwd error"}), 401

    if user.verify_passwd(passwd):
        token, timestamp = user.get_login_token()
        return flask.jsonify({"status": True, "message": "login success", "body": {"login_token": f"{timestamp}-{token}"}}), 200

    else:
        return flask.jsonify({"status": False, "message": "username or passwd error"}), 401


@api.route(get_endpoint() + "user/register", methods=["POST"])
def register():
    if not get_can_register():
        return flask.jsonify({"status": False, "message": "register is not allowed at the host"}), 403
    try:
        username = flask.request.json["username"]
        passwd = flask.request.json["passwd"]
    except KeyError as e:
        return flask.jsonify({"status": False, "message": "error request"}), 400
    try:
        user = actor.User.get(username)
        return flask.jsonify({"status": False, "message": "user already exists"}), 401
    except ValueError as e:
        user = actor.User.create(username, passwd)
        token, timestamp = user.get_login_token()
        return flask.jsonify({"status": True, "message": "register success", "body": {"login_token": f"{timestamp}-{token}"}}), 201


@api.route(get_endpoint() + "memo/sync", methods=["POST"])
def auto_sync():
    try:
        login_token = flask.request.json["login_token"]
        username = flask.request.json["username"]
        memo_content = flask.request.json["memo_content"]
        time = flask.request.json["time"]
        sync_method = flask.request.json["sync_method"]
    except KeyError as e:
        return flask.jsonify({"status": False, "message": "error request"}), 400

    try:
        timestamp, token = login_token.split("-")
    except ValueError as e:
        return flask.jsonify({"status": False, "message": "error login"}), 403
    timestamp = int(timestamp)
    s = sync.Sync(username)
    if s.verify(token, timestamp):
        if sync_method == "auto":
            result = s.auto_update(memo_content, time)
            if isinstance(result, actor.Memo):
                return flask.jsonify({"status": True, "message": "auto sync success", "body": {"memo_content": result.content, "time": result.update_time}}), 200
            else:
                return flask.jsonify({"status": True, "message": "auto sync success", "body": {"result": True}}), 200
        elif sync_method == "local":
            result = s.toLocal()
            return flask.jsonify({"status": True, "message": "local sync success", "body": {"memo_content": result.content, "time": result.update_time}}), 200
        elif sync_method == "remote":
            result = s.toRemote(memo_content, time)
            return flask.jsonify({"status": True, "message": "remote sync success", "body": {"result": result}}), 200
        else:
            return flask.jsonify({"status": False, "message": "error request"}), 400
    else:
        return flask.jsonify({"status": False, "message": "error login"}), 403


if __name__ == "__main__":
    api.run()
