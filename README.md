# 报价管理系统

一个基于Python Flask + Vue3 + Element Plus的报价管理系统，用于管理资源和生成报价单。

## 功能特性

### 资源管理
- 资源列表展示
- 新增资源
- 修改资源
- 删除资源
- 资源字段：id、名称、备注、单位、成本价、销售价

### 项目管理
- 项目列表展示
- 新增项目
- 修改项目
- 删除项目
- 项目字段：id、项目名称、项目日期
- 支持创建多个分组
- 每个分组支持关联多个资源
- 分组字段：id、项目id、分组名称
- 分组资源关联：分组id、资源id、数量
- **资源快照功能**：
  - 当用户进行新增或编辑操作时，使用资源对应金额的快照版本
  - 当删除关联资源，又再次添加关联资源时，使用资源的最新金额作为快照版本
  - 项目编辑，修改资源数量时，仍使用添加资源时的快照版本，不需要更新快照版本
  - 在项目详情和编辑弹框时，如果资源当前金额与快照版本不一致，使用红色字体进行提示，并显示警告图标

### 报价管理
- 报价列表展示
- 新增报价
- 修改报价
- 删除报价
- 报价字段：id、项目id（关联项目表）、日期、总成本、总销售价、利润
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
│   │   │   ├── QuotationView.vue
│   │   │   └── ProjectView.vue
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

### 项目接口
- `GET /api/projects` - 获取项目列表
- `POST /api/projects` - 新增项目
- `GET /api/projects/<id>` - 获取项目详情
- `PUT /api/projects/<id>` - 修改项目
- `DELETE /api/projects/<id>` - 删除项目

### 报价接口
- `GET /api/quotations` - 获取报价列表
- `POST /api/quotations` - 新增报价
- `GET /api/quotations/<id>` - 获取报价详情
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

### 项目分组表 (project_groups)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| project_id | INTEGER | 项目ID，外键 |
| group_name | TEXT | 分组名称 |

### 项目分组资源关联表 (project_group_resources)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| project_group_id | INTEGER | 分组ID，外键 |
| resource_id | INTEGER | 资源ID，外键 |
| quantity | INTEGER | 数量 |
| snapshot_cost_price | REAL | 成本价快照（新增时记录） |
| snapshot_sale_price | REAL | 销售价快照（新增时记录） |

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

## 资源快照功能说明

资源快照功能确保项目中的资源金额在添加时被记录，后续即使资源价格发生变化，项目中仍保留原始快照价格：

- **快照记录时机**：当资源被添加到项目分组时，自动记录当前资源的成本价和销售价作为快照
- **快照使用规则**：项目编辑时，修改资源数量不会影响已存在的快照价格
- **价格变动提示**：当资源的当前价格与快照价格不一致时，系统会在项目详情和编辑界面用红色字体提示，并显示警告图标
- **重新添加规则**：如果删除资源后重新添加，会使用最新的资源价格作为新的快照

此功能确保了项目成本核算的准确性和历史数据的一致性。

## 开发说明

- 后端使用Flask框架，SQLite数据库
- 前端使用Vue3 + Element Plus，Vite构建工具
- 前后端通过RESTful API进行通信
- 数据库表结构在models.py中定义
- API路由在routes.py中定义

## 许可证

MIT License
