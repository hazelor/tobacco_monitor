# coding=utf-8
from model.user import User
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def connect_db():
    import transwarp.db as dbutil
    dbutil.create_engine('sonic513', 'sonic513', 'tobacco_monitor', port=3307)

if __name__=="__main__":
    connect_db()
    if len(sys.argv)!=6:
        print "usage: python script/setting_add_user.py email password confirm_password permission(0,1) name"
    email = sys.argv[1]
    password = sys.argv[2]
    confirm_password = sys.argv[3]
    permission = sys.argv[4]
    name = sys.argv[5]
    usr = User(email = email, password=password, password_confirm = confirm_password, permission=permission, name=name)
    id= usr.create()
    if id:
        print "add user %s OK!" % name
    else:
        print usr.errors