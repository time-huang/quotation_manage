import sqlite3
from sqlite3 import Error

def create_connection():
    """ 创建数据库连接 """
    conn = None
    try:
        conn = sqlite3.connect('quotation_manage.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        print(e)
    return conn

def create_tables():
    """ 创建数据库表 """
    conn = create_connection()
    if conn is not None:
        # 创建资源表
        create_resources_table = ''' CREATE TABLE IF NOT EXISTS resources (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            name TEXT NOT NULL,
                                            remark TEXT,
                                            unit TEXT NOT NULL,
                                            cost_price REAL NOT NULL,
                                            sale_price REAL NOT NULL
                                        ); '''
        # 创建报价表
        create_quotations_table = ''' CREATE TABLE IF NOT EXISTS quotations (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            project_name TEXT NOT NULL,
                                            quote_date TEXT NOT NULL,
                                            total_cost REAL NOT NULL DEFAULT 0,
                                            total_sale REAL NOT NULL DEFAULT 0,
                                            profit REAL NOT NULL DEFAULT 0
                                        ); '''
        # 创建报价资源项表
        create_quotation_items_table = ''' CREATE TABLE IF NOT EXISTS quotation_items (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            quotation_id INTEGER NOT NULL,
                                            resource_id INTEGER NOT NULL,
                                            quantity INTEGER NOT NULL DEFAULT 1,
                                            FOREIGN KEY (quotation_id) REFERENCES quotations (id) ON DELETE CASCADE,
                                            FOREIGN KEY (resource_id) REFERENCES resources (id) ON DELETE CASCADE
                                        ); '''
        try:
            c = conn.cursor()
            c.execute(create_resources_table)
            c.execute(create_quotations_table)
            c.execute(create_quotation_items_table)
            conn.commit()
            print("Tables created successfully")
        except Error as e:
            print(e)
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    create_tables()
