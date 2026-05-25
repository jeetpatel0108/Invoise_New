from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, shop_name=None):
        self.id = id
        self.shop_name = shop_name
