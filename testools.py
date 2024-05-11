import hashlib

class Password:
    def set_password(self, raw_password):
        # 使用一个简单的加密方法，例如MD5
        encrypted_password = hashlib.md5(raw_password.encode()).hexdigest()
        self.password = encrypted_password




password = Password()
password.set_password('txy284013')
print(password.check_user_password('txy284013'))