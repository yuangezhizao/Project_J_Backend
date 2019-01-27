from main import create_app
from flask_script import Manager

# 创建app
app = create_app()
manager = Manager(app)

if __name__ == '__main__':
    """
    主函数启动http-server
    """
    manager.run()
