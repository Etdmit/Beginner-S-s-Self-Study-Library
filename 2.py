# 用户登录系统

# 模拟数据库中的用户信息（实际应用中会使用数据库）
users = {
    "admin": "123456",
    "zhangsan": "abc123",
    "lisi": "password",
    "wangwu": "888888"
}


def login():
    """用户登录函数"""
    print("=" * 40)
    print("       欢迎使用用户登录系统")
    print("=" * 40)

    # 输入用户名
    username = input("请输入用户名: ")

    # 检查用户名是否存在
    if username not in users:
        print("该用户不存在")
        return False

    # 输入密码
    password = input("请输入密码: ")

    # 验证密码是否正确
    if users[username] == password:
        print(f"登录成功，{username}欢迎你！")
        return True
    else:
        print("密码错误")
        return False


# 程序入口
if __name__ == "__main__":
    login()