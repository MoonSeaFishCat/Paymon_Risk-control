import logging
from API.API import main_api
from API.write_risk import write_word


def exit_system():
    # 这里定义退出系统的代码
    print("正在退出系统...")
    exit()


logging.info("欢迎使用Paymon风控处理终端")
logging.info("首次运行，请先添加风控词")
logging.info("请输入想要执行的操作")
logging.info("1,启动系统，2添加风控词，3退出系统")
key = str(input(""))
if key == "1":
    main_api()
elif key == "2":
    write_word()
elif key == "3":
    exit_system()
