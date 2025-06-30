import hashlib


def generate_account_md5(name: str, pwd: str, host: str) -> str:
    """
    根据账号密码和主机地址生成md5，防止重复导入分机账号
    """
    return hashlib.md5((name + pwd + host).encode("utf-8")).hexdigest()


if __name__ == "__main__":
    print(generate_account_md5("admin", "admin", "192.168.1.1"))
