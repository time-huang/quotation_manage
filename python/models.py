import sqlite3
from database import create_connection

class Project:
    """ 项目模型 """
    
    @staticmethod
    def get_all():
        """ 获取所有项目 """
        conn = create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("SELECT * FROM projects ORDER BY id DESC")
                projects = c.fetchall()
                return [dict(row) for row in projects]
            except sqlite3.Error as e:
                print(e)
                return []
            finally:
                conn.close()
        return []
    
    @staticmethod
    def get_by_id(project_id):
        """ 根据ID获取项目 """
        conn = create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
                project = c.fetchone()
                if not project:
                    return None
                project_dict = dict(project)
                project_dict['groups'] = []
                # 获取项目分组
                c.execute("SELECT * FROM project_groups WHERE project_id = ?", (project_id,))
                groups = c.fetchall()
                for group in groups:
                    group_dict = dict(group)
                    group_dict['resources'] = []
                    # 获取分组资源
                    c.execute("SELECT * FROM project_group_resources WHERE group_id = ?", (group_dict['id'],))
                    group_resources = c.fetchall()
                    for gr in group_resources:
                        gr_dict = dict(gr)
                        # 获取资源详情
                        c.execute("SELECT * FROM resources WHERE id = ?", (gr_dict['resource_id'],))
                        resource = c.fetchone()
                        if resource:
                            resource_dict = dict(resource)
                            resource_dict['quantity'] = gr_dict['quantity']
                            group_dict['resources'].append(resource_dict)
                    project_dict['groups'].append(group_dict)
                return project_dict
            except sqlite3.Error as e:
                print(e)
                return None
            finally:
                conn.close()
        return None
    
    @staticmethod
    def create(project_data):
        """ 创建项目 """
        conn = create_connection()
        if conn is not None:
            try:
                conn.execute('BEGIN TRANSACTION')
                
                # 创建项目主表
                c = conn.cursor()
                sql = ''' INSERT INTO projects(name, project_date)
                          VALUES(?,?) '''
                c.execute(sql, (project_data['name'], project_data['project_date']))
                project_id = c.lastrowid
                
                # 创建项目分组和资源
                if 'groups' in project_data and project_data['groups']:
                    for group in project_data['groups']:
                        # 创建分组
                        sql_group = ''' INSERT INTO project_groups(project_id, name)
                                      VALUES(?,?) '''
                        c.execute(sql_group, (project_id, group['name']))
                        group_id = c.lastrowid
                        
                        # 创建分组资源
                        if 'resources' in group and group['resources']:
                            for resource in group['resources']:
                                sql_resource = ''' INSERT INTO project_group_resources(group_id, resource_id, quantity)
                                                  VALUES(?,?,?) '''
                                c.execute(sql_resource, (group_id, resource['resource_id'], resource['quantity']))
                
                conn.commit()
                return project_id
            except sqlite3.Error as e:
                print(e)
                conn.rollback()
                return None
            finally:
                conn.close()
        return None
    
    @staticmethod
    def update(project_id, project_data):
        """ 更新项目 """
        conn = create_connection()
        if conn is not None:
            try:
                conn.execute('BEGIN TRANSACTION')
                
                # 更新项目主表
                c = conn.cursor()
                sql = ''' UPDATE projects
                          SET name = ?,
                              project_date = ?
                          WHERE id = ? '''
                c.execute(sql, (project_data['name'], project_data['project_date'], project_id))
                
                # 删除原有的分组和资源
                c.execute("DELETE FROM project_group_resources WHERE group_id IN (SELECT id FROM project_groups WHERE project_id = ?)", (project_id,))
                c.execute("DELETE FROM project_groups WHERE project_id = ?", (project_id,))
                
                # 创建新的项目分组和资源
                if 'groups' in project_data and project_data['groups']:
                    for group in project_data['groups']:
                        # 创建分组
                        sql_group = ''' INSERT INTO project_groups(project_id, name)
                                      VALUES(?,?) '''
                        c.execute(sql_group, (project_id, group['name']))
                        group_id = c.lastrowid
                        
                        # 创建分组资源
                        if 'resources' in group and group['resources']:
                            for resource in group['resources']:
                                sql_resource = ''' INSERT INTO project_group_resources(group_id, resource_id, quantity)
                                                  VALUES(?,?,?) '''
                                c.execute(sql_resource, (group_id, resource['resource_id'], resource['quantity']))
                
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
    def delete(project_id):
        """ 删除项目 """
        conn = create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("DELETE FROM projects WHERE id = ?", (project_id,))
                conn.commit()
                return c.rowcount > 0
            except sqlite3.Error as e:
                print(e)
                conn.rollback()
                return False
            finally:
                conn.close()
        return False

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
                sql = ''' INSERT INTO quotations(project_id, project_name, quote_date, total_cost, total_sale, profit)
                          VALUES(?,?,?,?,?,?) '''
                c.execute(sql, (quotation_data.get('project_id'), quotation_data['project_name'], quotation_data['quote_date'], 
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
                          SET project_id = ?,
                              project_name = ?,
                              quote_date = ?,
                              total_cost = ?,
                              total_sale = ?,
                              profit = ?
                          WHERE id = ? '''
                c.execute(sql, (quotation_data.get('project_id'), quotation_data['project_name'], quotation_data['quote_date'], 
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
