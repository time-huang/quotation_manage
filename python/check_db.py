import sqlite3

def check_database():
    conn = sqlite3.connect('quotation.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # 检查所有表
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    print('数据库表:', [table[0] for table in tables])
    
    # 检查项目数据
    c.execute('SELECT * FROM projects WHERE id = 2')
    project = c.fetchone()
    if project:
        print('项目数据:', dict(project))
        
        # 检查项目分组和资源
        c.execute('SELECT pg.name as group_name, r.name as resource_name, pgr.quantity, pgr.snapshot_cost_price, pgr.snapshot_sale_price FROM project_groups pg JOIN project_group_resources pgr ON pg.id = pgr.group_id JOIN resources r ON pgr.resource_id = r.id WHERE pg.project_id = 2')
        resources = c.fetchall()
        print('项目资源:')
        for res in resources:
            print(f'  分组: {res["group_name"]}, 资源: {res["resource_name"]}, 数量: {res["quantity"]}, 快照成本价: {res["snapshot_cost_price"]}, 快照销售价: {res["snapshot_sale_price"]}')
    else:
        print('未找到项目ID=2')
    
    conn.close()

if __name__ == '__main__':
    check_database()