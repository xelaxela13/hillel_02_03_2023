import json


class Store:

    def __init__(self):
        self.data = self._get_data()

    def _get_data(self):
        try:
            with open('users.json') as f:
                return json.load(f)
        except FileNotFoundError:
            self._add_data({'superuser@mail.com': {'password': '1234'}})

    def _add_data(self, data):
        with open('users.json', 'w') as f:
            json.dump(data, f)

    def check_user(self, email, password, is_login=True):
        user = self.data.get(email)
        if is_login:
            if not user:
                return False
            return user.get('password') == password
        return bool(user)

    def registration(self, email, password):
        data = self.data or self._get_data()
        data.update({email: {'password': password}})
        self._add_data(data)


store = Store()
