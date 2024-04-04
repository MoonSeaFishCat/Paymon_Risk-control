import sqlite3

def write_word():
    # 数据库文件名
    db_filename = '../data/plugins_risk_data.db'

    # 连接到SQLite数据库
    # 如果数据库文件不存在，会自动创建
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # 创建风险关键词表（如果尚不存在）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS risk_keywords (
        id INTEGER PRIMARY KEY,
        keyword TEXT NOT NULL UNIQUE
    )
    ''')

    # 提示用户输入风控词
    while True:
        risk_keyword = input("请输入风控词（输入'退出'结束输入）：")
        risk_keyword = risk_keyword.strip()
        if risk_keyword == '退出':
            break
        if risk_keyword:  # 确保风控词非空
            try:
                cursor.execute('INSERT INTO risk_keywords (keyword) VALUES (?)', (risk_keyword,))
                print(f"风控词 '{risk_keyword}' 已添加到数据库。")
            except sqlite3.IntegrityError:
                print(f"风控词 '{risk_keyword}' 已存在于数据库中。")

    # 提交事务
    conn.commit()

    # 关闭连接
    conn.close()

    print("所有风控词已添加完毕。")

