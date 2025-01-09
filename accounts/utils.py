import hashlib

class PasswordUtils:
    def encrypt_password(self, password):
        """加密密码"""
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        return md5.hexdigest()

    def validate_password(self, password, encrypted_password):
        """验证密码"""
        return self.encrypt_password(password) == encrypted_password
if __name__ == '__main__':
    # 使用示例
    utils = PasswordUtils()
    password = 'root'#数据库密码 执行后 把字符串复制回去
    encrypted = utils.encrypt_password(password)
    print(encrypted)  # e10adc3949ba59abbe56e057f20f883e

    result = utils.validate_password(password, encrypted)
    print(result)  # True