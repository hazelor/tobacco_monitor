#coding=utf-8
import transwarp.db
from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField
import time
import formencode
from formencode import validators
from util import hash_password

class User(Model):
    __table__ = 'user'

    id = StringField(primary_key=True, ddl='varchar(32)', default=next_id)
    email = StringField(updatable=False, ddl='varchar(50)')
    password = StringField(ddl='varchar(50)')
    permission = IntegerField()
    name = StringField(ddl='varchar(50)')
    created_at = FloatField(updatable=False, default=time.time)

    vali_email = validators.Email(not_empty = True,
                                    strip = True,
                                    messages = {'noAt': u'这可不是一个正常的邮箱',
                                                'empty': u'邮箱不能爲空'})
    vali_name = formencode.All(
            validators.String(
                 not_empty = True,
                 strip = True,
                 min = 4,
                 max = 24,
                 messages = {
                     'empty': u'用户名不能为空',
                     'tooLong': u'这么长的用户名没有必要吧',
                     'tooShort': u'用户名长度不能少于4'}),
             validators.PlainText(messages = {
                     'invalid': u'用户名只能包含数字，字母和下划线'
                  }))
    vali_password = validators.String(not_empty = True,
                                 messages = {'empty': u'忘记设置密码了'})
    vali_items = {'email': vali_email, 'name': vali_name, 'password': vali_password}

    def validate(self):
        self.errors = {}
        for k, vali in self.vali_items.items():
            try:
                vali.to_python(self[k])
            except formencode.Invalid as e:
                self.errors[k] = e

        if self.errors:
            return False
        return True

    def create(self):
        self.created_at = time.time()
        if not self.validate():
            return
        if User.find_first('where email = ?', self.email):
            self.errors = {'email': u'此email已被占用'}
            return
        if User.find_first('where name = ?', self.name):
            self.errors = {'name': u'此用戶名已被注冊'}
            return
        if not self.password_confirm:
            self.errors = {'password_confirm': u'确认密码不能为空'}
            return
        if self.password != self.password_confirm:
            self.errors = {'password': u'兩次密碼輸入不一致'}
            return
        self.password = hash_password(self.password)
        self.insert()
        return self.id

    def change_password(self, origin_password, password, password_confirm):
        if not origin_password:
            self.errors['origin_password'] = u'当前密码不能为空'

        if not password:
            self.errors['password'] = u'密码不能为空'

        if not password_confirm:
            self.errors['password_confirm'] = u'确认密码不能为空'

        if password!= password_confirm:
            self.errors['password_confirm'] = u'两次密码不一致'

        if self.errors:
            return False

        self.password = hash_password(self.password)

        self.update()



