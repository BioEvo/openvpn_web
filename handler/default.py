# -- coding: utf8 --
import json
import os
import sys
from hashlib import md5
import time
import base64

from model.default import User, Admin, Logs

from . import BaseHandler


def CheckLogin(func):
    def wrapper(self, *args, **kwargs):
        query = Admin.select().where(Admin.username == self.get_cookie("username")).first()
        if query is not None:
            if self.get_cookie("token") == query.token.strip():
                return func(self, *args, **kwargs)
        self.send_error(status_code=401)
    return wrapper


class LoginHandler(BaseHandler):
    def get(self):
        query = Admin.select().where(Admin.username == self.get_cookie("username")).first()
        if query is not None:
            if self.get_cookie("token") == query.token.strip():
                self.redirect("/")
        else:
            self.render("login.html")

    def post(self):
        req = json.loads(self.request.body)
        admin = Admin.select().where(Admin.username == req['username']).first()
        if admin is not None:
            if req['password'] == admin.password:
                if sys.version_info.major == 3:
                    token = base64.encodebytes((req['username'] + str(time.time())).encode()).decode()
                if sys.version_info.major == 2:
                    token = base64.encodestring(req['username'] + str(time.time()))
                admin = Admin.update({Admin.token: token}).where(Admin.username == req['username'])
                admin.execute()
                self.write(json.dumps({"result": "登陆成功", "token": token, "code": 0}))
            else:
                self.write(json.dumps({"result": "密码不正确", "code": -1}))
        else:
            err_msg = {"result": "%s 用户不存在" % req['username']}
            self.send_error(status_code=400, **err_msg)


class MainHandler(BaseHandler):
    def get(self):
        if self.get_cookie("username") is not None:
            self.render("index.html")
        else:
            self.redirect("/login")


class AdminHandler(BaseHandler):
    def post(self):
        req = json.loads(self.request.body)
        admin = Admin.update({Admin.password: req['password']}).where(Admin.username == "admin")
        admin.execute()
        self.write(json.dumps({"result": "success"}))


class UserHandler(BaseHandler):
    @CheckLogin
    def get(self):
        user = self.get_query_arguments("user")[0]
        page = int(self.get_query_arguments("page")[0])
        pagenum = int(self.get_query_arguments("limit")[0])

        result = {"status": 0, "message": "", "total": 0, "data": {}}
        data = {}
        node = []
        if user == "all":
            total = User.select().count()
            result['total'] = total

            query = User.select().order_by(User.id).limit(pagenum).offset((page - 1)*pagenum)
            for item in query:
                userinfo = {}
                userinfo['id'] = item.id
                userinfo['username'] = item.username
                userinfo['password'] = item.password
                if item.active == 1:
                    userinfo['active'] = True
                else:
                    userinfo['active'] = False
                userinfo['expire'] = item.expire
                userinfo['firewall'] = item.firewall
                node.append(userinfo)
            data['item'] = node
            result['data'] = data
            self.write(json.dumps(result))
        else:
            total = User.select().where(User.username.contains(user)).count()
            result['total'] = total

            query = User.select().where(User.username.contains(user)).order_by(User.id).limit(pagenum).offset((page - 1)*pagenum)
            for item in query:
                userinfo = {}
                userinfo['id'] = item.id
                userinfo['username'] = item.username
                userinfo['password'] = item.password
                if item.active == 1:
                    userinfo['active'] = True
                else:
                    userinfo['active'] = False
                userinfo['expire'] = item.expire
                userinfo['firewall'] = item.firewall
                node.append(userinfo)
            data['item'] = node
            result['data'] = data
            self.write(json.dumps(result))

class AddHandler(BaseHandler):
    @CheckLogin
    def post(self):
        req = json.loads(self.request.body)
        query = User.select().where(User.username == req['username']).first()
        if query is None:
            insert = User.insert(req)
            insert.execute()
            self.write(json.dumps({"result": "success"}))
        else:
            err_msg = {"result": "%s 已经存在" % query.username}
            self.send_error(status_code=500, **err_msg)


class UpdateHandler(BaseHandler):
    @CheckLogin
    def post(self):
        req = json.loads(self.request.body)
        for key, value in req.items():
            if key == 'password':
                user = User.update({User.password: value}).where(User.id == req['id'])
                user.execute()
            if key == 'active':
                user = User.update({User.active: value}).where(User.id == req['id'])
                user.execute()
            if key == 'expire':
                user = User.update({User.expire: value}).where(User.id == req['id'])
                user.execute()
            if key == 'firewall':
                user = User.update({User.firewall: value}).where(User.id == req['id'])
                user.execute()
        self.write(json.dumps({"result": "success"}))


class DelHandler(BaseHandler):
    @CheckLogin
    def post(self):
        req = json.loads(self.request.body)
        query = User.select(User.username).where(User.id == req['id']).first()
        user = User.delete().where(User.id == req['id'])
        user.execute()
        if query is not None:
            log = Logs.delete().where(Logs.username == query.username)
            log.execute()
        self.write(json.dumps({"result": "success"}))


class LogsHandler(BaseHandler):
    @CheckLogin
    def get(self):
        user = self.get_query_arguments("user")[0]
        page = int(self.get_query_arguments("page")[0])
        pagenum = int(self.get_query_arguments("limit")[0])

        result = {"status": 0, "message": "", "total": 0, "data": {}}
        data = {}
        node = []

        if user == "all":
            total = Logs.select().count()
            result['total'] = total
            query = Logs.select().order_by(Logs.id).limit(pagenum).offset((page - 1)*pagenum)
            for item in query:
                loginfo = {}
                loginfo['id'] = item.id
                loginfo['username'] = item.username
                loginfo['local'] = item.local
                loginfo['remote'] = item.remote
                loginfo['trusted_ip'] = item.trusted_ip
                loginfo['trusted_port'] = item.trusted_port
                loginfo['logintime'] = item.logintime
                loginfo['logouttime'] = item.logouttime
                loginfo['received'] = item.received
                loginfo['sent'] = item.sent
                node.append(loginfo)
            data['item'] = node
            result['data'] = data
            self.write(json.dumps(result))
        else:
            total = Logs.select().where(Logs.username == user).count()
            result['total'] = total
            query = Logs.select().where(Logs.username == user).order_by(Logs.id).limit(pagenum).offset((page - 1)*pagenum)
            for item in query:
                loginfo = {}
                loginfo['id'] = item.id
                loginfo['username'] = item.username
                loginfo['local'] = item.local
                loginfo['remote'] = item.remote
                loginfo['trusted_ip'] = item.trusted_ip
                loginfo['trusted_port'] = item.trusted_port
                loginfo['logintime'] = item.logintime
                loginfo['logouttime'] = item.logouttime
                loginfo['received'] = item.received
                loginfo['sent'] = item.sent
                node.append(loginfo)
            data['item'] = node
            result['data'] = data
            self.write(json.dumps(result))
