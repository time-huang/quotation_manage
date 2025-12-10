from flask import Blueprint, request, jsonify
from models import Resource, Quotation, Project

api_bp = Blueprint('api', __name__)

# 项目相关路由
@api_bp.route('/projects', methods=['GET'])
def get_projects():
    """ 获取所有项目 """
    projects = Project.get_all()
    return jsonify({'success': True, 'data': projects})

@api_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """ 根据ID获取项目 """
    project = Project.get_by_id(project_id)
    if project:
        return jsonify({'success': True, 'data': project})
    else:
        return jsonify({'success': False, 'message': 'Project not found'}), 404

@api_bp.route('/projects', methods=['POST'])
def create_project():
    """ 创建项目 """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    # 验证必填字段
    required_fields = ['name', 'project_date']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
    
    project_id = Project.create(data)
    if project_id:
        project = Project.get_by_id(project_id)
        return jsonify({'success': True, 'data': project}), 201
    else:
        return jsonify({'success': False, 'message': 'Failed to create project'}), 500

@api_bp.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """ 更新项目 """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    # 验证项目是否存在
    existing_project = Project.get_by_id(project_id)
    if not existing_project:
        return jsonify({'success': False, 'message': 'Project not found'}), 404
    
    # 验证必填字段
    required_fields = ['name', 'project_date']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
    
    success = Project.update(project_id, data)
    if success:
        project = Project.get_by_id(project_id)
        return jsonify({'success': True, 'data': project})
    else:
        return jsonify({'success': False, 'message': 'Failed to update project'}), 500

@api_bp.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """ 删除项目 """
    # 验证项目是否存在
    existing_project = Project.get_by_id(project_id)
    if not existing_project:
        return jsonify({'success': False, 'message': 'Project not found'}), 404
    
    success = Project.delete(project_id)
    if success:
        return jsonify({'success': True, 'message': 'Project deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to delete project'}), 500

# 资源相关路由
@api_bp.route('/resources', methods=['GET'])
def get_resources():
    """ 获取所有资源 """
    resources = Resource.get_all()
    return jsonify({'success': True, 'data': resources})

@api_bp.route('/resources/<int:resource_id>', methods=['GET'])
def get_resource(resource_id):
    """ 根据ID获取资源 """
    resource = Resource.get_by_id(resource_id)
    if resource:
        return jsonify({'success': True, 'data': resource})
    else:
        return jsonify({'success': False, 'message': 'Resource not found'}), 404

@api_bp.route('/resources', methods=['POST'])
def create_resource():
    """ 创建资源 """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    # 验证必填字段
    required_fields = ['name', 'unit', 'cost_price', 'sale_price']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
    
    # 验证价格是否为正数
    if float(data['cost_price']) <= 0 or float(data['sale_price']) <= 0:
        return jsonify({'success': False, 'message': 'Price must be positive'}), 400
    
    resource_id = Resource.create(data)
    if resource_id:
        resource = Resource.get_by_id(resource_id)
        return jsonify({'success': True, 'data': resource}), 201
    else:
        return jsonify({'success': False, 'message': 'Failed to create resource'}), 500

@api_bp.route('/resources/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    """ 更新资源 """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    # 验证资源是否存在
    existing_resource = Resource.get_by_id(resource_id)
    if not existing_resource:
        return jsonify({'success': False, 'message': 'Resource not found'}), 404
    
    # 验证价格是否为正数
    if 'cost_price' in data and float(data['cost_price']) <= 0:
        return jsonify({'success': False, 'message': 'Cost price must be positive'}), 400
    if 'sale_price' in data and float(data['sale_price']) <= 0:
        return jsonify({'success': False, 'message': 'Sale price must be positive'}), 400
    
    success = Resource.update(resource_id, data)
    if success:
        resource = Resource.get_by_id(resource_id)
        return jsonify({'success': True, 'data': resource})
    else:
        return jsonify({'success': False, 'message': 'Failed to update resource'}), 500

@api_bp.route('/resources/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    """ 删除资源 """
    # 验证资源是否存在
    existing_resource = Resource.get_by_id(resource_id)
    if not existing_resource:
        return jsonify({'success': False, 'message': 'Resource not found'}), 404
    
    success = Resource.delete(resource_id)
    if success:
        return jsonify({'success': True, 'message': 'Resource deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to delete resource'}), 500

# 报价相关路由
@api_bp.route('/quotations', methods=['GET'])
def get_quotations():
    """ 获取所有报价 """
    quotations = Quotation.get_all()
    return jsonify({'success': True, 'data': quotations})

@api_bp.route('/quotations/<int:quotation_id>', methods=['GET'])
def get_quotation(quotation_id):
    """ 根据ID获取报价 """
    quotation = Quotation.get_by_id(quotation_id)
    if quotation:
        return jsonify({'success': True, 'data': quotation})
    else:
        return jsonify({'success': False, 'message': 'Quotation not found'}), 404

@api_bp.route('/quotations', methods=['POST'])
def create_quotation():
    """ 创建报价 """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    # 验证必填字段
    required_fields = ['project_name', 'quote_date', 'items']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
    
    # 验证items是否为非空数组
    if not isinstance(data['items'], list) or len(data['items']) == 0:
        return jsonify({'success': False, 'message': 'Items must be a non-empty array'}), 400
    
    # 验证每个item的必填字段
    for item in data['items']:
        if 'resource_id' not in item or 'quantity' not in item:
            return jsonify({'success': False, 'message': 'Each item must have resource_id and quantity'}), 400
        if int(item['quantity']) <= 0:
            return jsonify({'success': False, 'message': 'Item quantity must be positive'}), 400
    
    # 计算总成本、总销售价和利润
    total_cost = 0
    total_sale = 0
    
    for item in data['items']:
        resource = Resource.get_by_id(item['resource_id'])
        if not resource:
            return jsonify({'success': False, 'message': f'Resource not found: {item["resource_id"]}'}), 404
        
        quantity = int(item['quantity'])
        total_cost += resource['cost_price'] * quantity
        total_sale += resource['sale_price'] * quantity
    
    profit = total_sale - total_cost
    
    # 添加计算后的字段到数据
    data['total_cost'] = total_cost
    data['total_sale'] = total_sale
    data['profit'] = profit
    
    quotation_id = Quotation.create(data)
    if quotation_id:
        quotation = Quotation.get_by_id(quotation_id)
        return jsonify({'success': True, 'data': quotation}), 201
    else:
        return jsonify({'success': False, 'message': 'Failed to create quotation'}), 500

@api_bp.route('/quotations/<int:quotation_id>', methods=['PUT'])
def update_quotation(quotation_id):
    """ 更新报价 """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    # 验证报价是否存在
    existing_quotation = Quotation.get_by_id(quotation_id)
    if not existing_quotation:
        return jsonify({'success': False, 'message': 'Quotation not found'}), 404
    
    # 如果有items字段，验证items
    if 'items' in data:
        if not isinstance(data['items'], list) or len(data['items']) == 0:
            return jsonify({'success': False, 'message': 'Items must be a non-empty array'}), 400
        
        # 验证每个item的必填字段
        for item in data['items']:
            if 'resource_id' not in item or 'quantity' not in item:
                return jsonify({'success': False, 'message': 'Each item must have resource_id and quantity'}), 400
            if int(item['quantity']) <= 0:
                return jsonify({'success': False, 'message': 'Item quantity must be positive'}), 400
        
        # 计算总成本、总销售价和利润
        total_cost = 0
        total_sale = 0
        
        for item in data['items']:
            resource = Resource.get_by_id(item['resource_id'])
            if not resource:
                return jsonify({'success': False, 'message': f'Resource not found: {item["resource_id"]}'}), 404
            
            quantity = int(item['quantity'])
            total_cost += resource['cost_price'] * quantity
            total_sale += resource['sale_price'] * quantity
        
        profit = total_sale - total_cost
        
        # 添加计算后的字段到数据
        data['total_cost'] = total_cost
        data['total_sale'] = total_sale
        data['profit'] = profit
    
    success = Quotation.update(quotation_id, data)
    if success:
        quotation = Quotation.get_by_id(quotation_id)
        return jsonify({'success': True, 'data': quotation})
    else:
        return jsonify({'success': False, 'message': 'Failed to update quotation'}), 500

@api_bp.route('/quotations/<int:quotation_id>', methods=['DELETE'])
def delete_quotation(quotation_id):
    """ 删除报价 """
    # 验证报价是否存在
    existing_quotation = Quotation.get_by_id(quotation_id)
    if not existing_quotation:
        return jsonify({'success': False, 'message': 'Quotation not found'}), 404
    
    success = Quotation.delete(quotation_id)
    if success:
        return jsonify({'success': True, 'message': 'Quotation deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to delete quotation'}), 500

@api_bp.route('/quotations/<int:quotation_id>/items', methods=['GET'])
def get_quotation_items(quotation_id):
    """ 获取报价的资源项 """
    # 验证报价是否存在
    existing_quotation = Quotation.get_by_id(quotation_id)
    if not existing_quotation:
        return jsonify({'success': False, 'message': 'Quotation not found'}), 404
    
    items = Quotation.get_items(quotation_id)
    return jsonify({'success': True, 'data': items})
