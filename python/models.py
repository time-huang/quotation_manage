import sqlite3
from database import create_connection

class Resource:
    """ 资源模型 """
    
    @staticmethod
    def get_all():
        """ 获取所有资源 """
        conn = create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("SELECT * FROM resources ORDER BY id DESC")
                resources = c.fetchall()
                return [dict(row) for row in resources]
            except sqlite3.Error as e:
                print(e)
                return []
            finally:
                conn.close()
        return []
    
    @staticmethod
    def get_by_id(resource_id):
        """ 根据ID获取资源 """
        conn = create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("SELECT * FROM resources WHERE id = ?", (resource_id,))
                resource = c.fetchone()
                return dict(resource) if resource else None
            except sqlite3.Error as e:
                print(e)
                return None
            finally:
                conn.close()
        return None
    
    @staticmethod
    def create(resource_data):
        """ 创建资源 """
        conn = create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                sql = ''' INSERT INTO resources(name,remark,unit,cost_price,sale_price)
                          VALUES(?,?,?,?,?) '''
                c.execute(sql, (resource_data['name'], resource_data.get('remark', ''), 
                                resource_data['unit'], resource_data['cost_price'], 
                                resource_data['sale_price']))
                conn.commit()
                return c.lastrowid
            except sqlite3.Error as e:
                print(e)
                conn.rollback()
                return None
            finally:
                conn.close()
        return None
    
    @staticmethod
    def update(resource_id, resource_data):
        """ 更新资源 """
        conn = create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                sql = ''' UPDATE resources
                          SET name = ?,
                              remark = ?,
                              unit = ?,
                              cost_price = ?,
                              sale_price = ?
                          WHERE id = ? '''
                c.execute(sql, (resource_data['name'], resource_data.get('remark', ''), 
                                resource_data['unit'], resource_data['cost_price'], 
                                resource_data['sale_price'], resource_id))
                conn.commit()
                return c.rowcount > 0
            except sqlite3.Error as e:
                print(e)
                conn.rollback()
                return False
            finally:
                conn.close()
        return False
    
    @staticmethod
    def delete(resource_id):
        """ 删除资源 """
        conn = create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("DELETE FROM resources WHERE id = ?", (resource_id,))
                conn.commit()
                return c.rowcount > 0
            except sqlite3.Error as e:
                print(e)
                conn.rollback()
                return False
            finally:
                conn.close()
        return False

class Quotation:
    """ 报价模型 """
    
    @staticmethod
    def get_all():
        """ 获取所有报价 """
        conn = create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("SELECT * FROM quotations ORDER BY id DESC")
                quotations = c.fetchall()
                return [dict(row) for row in quotations]
            except sqlite3.Error as e:
                print(e)
                return []
            finally:
                conn.close()
        return []
    
    @staticmethod
    def get_by_id(quotation_id):
        """ 根据ID获取报价 """
        conn = create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("SELECT * FROM quotations WHERE id = ?", (quotation_id,))
                quotation = c.fetchone()
                return dict(quotation) if quotation else None
            except sqlite3.Error as e:
                print(e)
                return None
            finally:
                conn.close()
        return None
    
    @staticmethod
    def create(quotation_data):
        """ 创建报价 """
        conn = create_connection()
        if conn is not None:
            try:
                conn.execute('BEGIN TRANSACTION')
                
                # 创建报价主表
                c = conn.cursor()
                sql = ''' INSERT INTO quotations(project_name,quote_date,total_cost,total_sale,profit)
                          VALUES(?,?,?,?,?) '''
                c.execute(sql, (quotation_data['project_name'], quotation_data['quote_date'], 
                                quotation_data['total_cost'], quotation_data['total_sale'], 
                                quotation_data['profit']))
                quotation_id = c.lastrowid
                
                # 创建报价资源项
                if 'items' in quotation_data and quotation_data['items']:
                    for item in quotation_data['items']:
                        sql_item = ''' INSERT INTO quotation_items(quotation_id,resource_id,quantity)
                                      VALUES(?,?,?) '''
                        c.execute(sql_item, (quotation_id, item['resource_id'], item['quantity']))
                
                conn.commit()
                return quotation_id
            except sqlite3.Error as e:
                print(e)
                conn.rollback()
                return None
            finally:
                conn.close()
        return None
    
    @staticmethod
    def update(quotation_id, quotation_data):
        """ 更新报价 """
        conn = create_connection()
        if conn is not None:
            try:
                conn.execute('BEGIN TRANSACTION')
                
                # 更新报价主表
                c = conn.cursor()
                sql = ''' UPDATE quotations
                          SET project_name = ?,
                              quote_date = ?,
                              total_cost = ?,
                              total_sale = ?,
                              profit = ?
                          WHERE id = ? '''
                c.execute(sql, (quotation_data['project_name'], quotation_data['quote_date'], 
                                quotation_data['total_cost'], quotation_data['total_sale'], 
                                quotation_data['profit'], quotation_id))
                
                # 删除原有的报价资源项
                sql_delete_items = "DELETE FROM quotation_items WHERE quotation_id = ?"
                c.execute(sql_delete_items, (quotation_id,))
                
                # 添加新的报价资源项
                if 'items' in quotation_data and quotation_data['items']:
                    for item in quotation_data['items']:
                        sql_item = ''' INSERT INTO quotation_items(quotation_id,resource_id,quantity)
                                      VALUES(?,?,?) '''
                        c.execute(sql_item, (quotation_id, item['resource_id'], item['quantity']))
                
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(e)
                conn.rollback()
                return False
            finally:
                conn.close()
        return False
    
    @staticmethod
    def delete(quotation_id):
        """ 删除报价 """
        conn = create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("DELETE FROM quotations WHERE id = ?", (quotation_id,))
                conn.commit()
                return c.rowcount > 0
            except sqlite3.Error as e:
                print(e)
                conn.rollback()
                return False
            finally:
                conn.close()
        return False
    
    @staticmethod
    def get_items(quotation_id):
        """ 获取报价的资源项 """
        conn = create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                sql = ''' SELECT qi.*, r.name, r.unit, r.cost_price, r.sale_price
                          FROM quotation_items qi
                          JOIN resources r ON qi.resource_id = r.id
                          WHERE qi.quotation_id = ? '''
                c.execute(sql, (quotation_id,))
                items = c.fetchall()
                return [dict(row) for row in items]
            except sqlite3.Error as e:
                print(e)
                return []
            finally:
                conn.close()
        return []
