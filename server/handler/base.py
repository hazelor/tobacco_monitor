__author__ = 'sonic-server'

# import tornado
import tornado.web

class base_handler(tornado.web.RequestHandler):
    def send_error_json(self, data):
        return self.write({
            'status': 'error',
            'content': data
            })

    def send_success_json(self, **data):
        return self.write({
            'status': 'ok',
            'content': data
            })

    def get_current_user(self):
        user_id = self.get_secure_cookie('u_u')
        if not user_id:
            return None
        import model
        u = model.user.User().find_first("where id = ?", user_id)
        if not u:
            return None
        return u

    def is_admin(self):
        usr = self.get_current_user()
         if usr.permission != PERMISSION_ADMIN:
            return False
        else:
            return True