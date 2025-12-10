# 报价管理系统

一个基于Python Flask + Vue3 + Element Plus的报价管理系统，用于管理资源和生成报价单。

## 功能特性

### 资源管理
- 资源列表展示
- 新增资源
- 修改资源
- 删除资源
- 资源字段：id、名称、备注、单位、成本价、销售价

### 报价管理
- 报价列表展示
- 新增报价
- 修改报价
- 删除报价
- 报价字段：id、项目名称、日期、总成本、总销售价、利润
- 支持关联多个资源作为子表

## 技术栈

### 后端
- Python 3.8+
- Flask 2.0+
- Flask-CORS 3.0+
- SQLite 3

### 前端
- Vue 3
- Element Plus
- Axios

## 项目结构

```
quotation_manage/
├── python/                 # 后端目录
│   ├── app.py             # Flask应用主文件
│   ├── models.py           # 数据库模型
│   ├── routes.py           # API路由
│   ├── database.py         # 数据库连接
│   └── requirements.txt     # Python依赖
├── web/                    # 前端目录
│   ├── src/
│   │   ├── main.js        # Vue应用入口
│   │   ├── App.vue        # 根组件
│   │   ├── components/     # 组件目录
│   │   │   ├── ResourceList.vue
│   │   │   ├── ResourceForm.vue
│   │   │   ├── QuotationList.vue
│   │   │   └── QuotationForm.vue
│   │   ├── views/          # 页面目录
│   │   │   ├── ResourceView.vue
│   │   │   └── QuotationView.vue
│   │   ├── router/         # 路由配置
│   │   │   └── index.js
│   │   └── utils/          # 工具函数
│   │       └── request.js
│   ├── public/
│   ├── package.json         # Node.js依赖
│   └── vite.config.js       # Vite配置
└── README.md                # 项目说明
```

## 安装与运行

### 后端安装

```bash
cd python
pip install -r requirements.txt
python app.py
```

后端服务将在 http://localhost:5000 启动

### 前端安装

```bash
cd web
npm install
npm run dev
```

前端服务将在 http://localhost:5173 启动

## API接口

### 资源接口
- `GET /api/resources` - 获取资源列表
- `POST /api/resources` - 新增资源
- `PUT /api/resources/<id>` - 修改资源
- `DELETE /api/resources/<id>` - 删除资源

### 报价接口
- `GET /api/quotations` - 获取报价列表
- `POST /api/quotations` - 新增报价
- `PUT /api/quotations/<id>` - 修改报价
- `DELETE /api/quotations/<id>` - 删除报价
- `GET /api/quotations/<id>/items` - 获取报价资源项

## 数据库设计

### 资源表 (resources)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| name | TEXT | 资源名称 |
| remark | TEXT | 备注 |
| unit | TEXT | 单位 |
| cost_price | REAL | 成本价 |
| sale_price | REAL | 销售价 |

### 报价表 (quotations)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| project_name | TEXT | 项目名称 |
| quote_date | TEXT | 报价日期 |
| total_cost | REAL | 总成本 |
| total_sale | REAL | 总销售价 |
| profit | REAL | 利润 |

### 报价资源项表 (quotation_items)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| quotation_id | INTEGER | 报价ID，外键 |
| resource_id | INTEGER | 资源ID，外键 |
| quantity | INTEGER | 数量 |

## 使用说明

1. 启动后端服务
2. 启动前端服务
3. 在浏览器中访问前端地址
4. 先添加资源，再创建报价单
5. 创建报价单时可以选择多个资源并设置数量

## 开发说明

- 后端使用Flask框架，SQLite数据库
- 前端使用Vue3 + Element Plus，Vite构建工具
- 前后端通过RESTful API进行通信
- 数据库表结构在models.py中定义
- API路由在routes.py中定义

## 许可证

MIT License
