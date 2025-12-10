<template>
  <div class="quotation-view">
    <el-card class="quotation-card">
      <template #header>
        <div class="card-header">
          <span>报价管理</span>
          <el-button type="primary" @click="openAddDialog">
            <el-icon><Plus /></el-icon>
            新增报价
          </el-button>
        </div>
      </template>
      
      <!-- 报价列表 -->
      <el-table :data="quotationList" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="project_name" label="项目名称" />
        <el-table-column prop="quote_date" label="报价日期" width="150" />
        <el-table-column prop="total_cost" label="总成本" width="120">
          <template #default="{ row }">
            {{ row.total_cost.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="total_sale" label="总销售价" width="120">
          <template #default="{ row }">
            {{ row.total_sale.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="profit" label="利润" width="120">
          <template #default="{ row }">
            <span :class="{ 'profit-positive': row.profit >= 0, 'profit-negative': row.profit < 0 }">
              {{ row.profit.toFixed(2) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewQuotationItems(row.id)">
              <el-icon><View /></el-icon>
              查看明细
            </el-button>
            <el-button type="warning" size="small" @click="openEditDialog(row)">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteQuotation(row.id)">
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 新增/编辑报价对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="800px"
      @close="closeDialog"
    >
      <el-form
        ref="quotationForm"
        :model="formData"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="项目名称" prop="project_name">
          <el-input v-model="formData.project_name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="报价日期" prop="quote_date">
          <el-date-picker
            v-model="formData.quote_date"
            type="date"
            placeholder="请选择报价日期"
            style="width: 100%"
          />
        </el-form-item>
        
        <!-- 资源项选择 -->
        <el-form-item label="资源项">
          <div class="resource-item-selector">
            <!-- 资源选择 -->
            <el-select
              v-model="selectedResourceId"
              placeholder="请选择资源"
              style="width: 200px; margin-right: 10px"
            >
              <el-option
                v-for="resource in resourceList"
                :key="resource.id"
                :label="resource.name"
                :value="resource.id"
              />
            </el-select>
            
            <!-- 数量输入 -->
            <el-input
              v-model.number="resourceQuantity"
              placeholder="请输入数量"
              style="width: 100px; margin-right: 10px"
            />
            
            <!-- 添加按钮 -->
            <el-button type="primary" @click="addResourceItem">
              <el-icon><Plus /></el-icon>
              添加
            </el-button>
          </div>
          
          <!-- 已选择的资源项 -->
          <el-table :data="formData.items" style="width: 100%; margin-top: 10px" border>
            <el-table-column prop="name" label="资源名称" />
            <el-table-column prop="unit" label="单位" width="100" />
            <el-table-column prop="cost_price" label="成本价" width="100">
              <template #default="{ row }">
                {{ row.cost_price.toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column prop="sale_price" label="销售价" width="100">
              <template #default="{ row }">
                {{ row.sale_price.toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量" width="100" />
            <el-table-column prop="sub_total_cost" label="分项成本" width="120">
              <template #default="{ row }">
                {{ row.sub_total_cost.toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column prop="sub_total_sale" label="分项销售价" width="140">
              <template #default="{ row }">
                {{ row.sub_total_sale.toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100">
              <template #default="{ row, $index }">
                <el-button type="danger" size="small" @click="removeResourceItem($index)">
                  <el-icon><Delete /></el-icon>
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closeDialog">取消</el-button>
          <el-button type="primary" @click="saveQuotation">保存</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 报价明细对话框 -->
    <el-dialog
      v-model="itemsDialogVisible"
      title="报价明细"
      width="800px"
      @close="closeItemsDialog"
    >
      <el-table :data="quotationItems" style="width: 100%" border>
        <el-table-column prop="name" label="资源名称" />
        <el-table-column prop="unit" label="单位" width="100" />
        <el-table-column prop="cost_price" label="成本价" width="100">
          <template #default="{ row }">
            {{ row.cost_price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="sale_price" label="销售价" width="100">
          <template #default="{ row }">
            {{ row.sale_price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="quantity" label="数量" width="100" />
        <el-table-column prop="sub_total_cost" label="分项成本" width="120">
          <template #default="{ row }">
            {{ (row.cost_price * row.quantity).toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="sub_total_sale" label="分项销售价" width="140">
          <template #default="{ row }">
            {{ (row.sale_price * row.quantity).toFixed(2) }}
          </template>
        </el-table-column>
      </el-table>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closeItemsDialog">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Delete, View } from '@element-plus/icons-vue'
import request from '../utils/request'

// 响应式数据
const quotationList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 对话框相关
const dialogVisible = ref(false)
const dialogTitle = ref('新增报价')
const editingQuotation = ref(null)

// 报价明细对话框
const itemsDialogVisible = ref(false)
const quotationItems = ref([])

// 表单数据
const formData = reactive({
  project_name: '',
  quote_date: '',
  items: []
})

// 表单引用
const quotationForm = ref(null)

// 资源选择相关
const resourceList = ref([])
const selectedResourceId = ref('')
const resourceQuantity = ref(1)

// 表单验证规则
const formRules = reactive({
  project_name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' }
  ],
  quote_date: [
    { required: true, message: '请选择报价日期', trigger: 'change' }
  ]
})

// 生命周期钩子
onMounted(() => {
  fetchQuotations()
  fetchResources()
})

// 获取报价列表
const fetchQuotations = async () => {
  try {
    const data = await request.get('/quotations')
    quotationList.value = data
    total.value = data.length
  } catch (error) {
    ElMessage.error('获取报价列表失败: ' + error.message)
  }
}

// 获取资源列表
const fetchResources = async () => {
  try {
    const data = await request.get('/resources')
    resourceList.value = data
  } catch (error) {
    ElMessage.error('获取资源列表失败: ' + error.message)
  }
}

// 打开新增对话框
const openAddDialog = () => {
  dialogTitle.value = '新增报价'
  editingQuotation.value = null
  resetForm()
  dialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = async (quotation) => {
  dialogTitle.value = '编辑报价'
  editingQuotation.value = quotation
  
  // 填充表单数据
  formData.project_name = quotation.project_name
  formData.quote_date = quotation.quote_date
  
  // 获取报价明细
  try {
    const items = await request.get(`/quotations/${quotation.id}/items`)
    formData.items = items.map(item => ({
      resource_id: item.resource_id,
      name: item.name,
      unit: item.unit,
      cost_price: item.cost_price,
      sale_price: item.sale_price,
      quantity: item.quantity,
      sub_total_cost: item.cost_price * item.quantity,
      sub_total_sale: item.sale_price * item.quantity
    }))
  } catch (error) {
    ElMessage.error('获取报价明细失败: ' + error.message)
  }
  
  dialogVisible.value = true
}

// 关闭对话框
const closeDialog = () => {
  dialogVisible.value = false
  resetForm()
}

// 重置表单
const resetForm = () => {
  formData.project_name = ''
  formData.quote_date = ''
  formData.items = []
  selectedResourceId.value = ''
  resourceQuantity.value = 1
  
  // 重置表单验证
  if (quotationForm.value) {
    quotationForm.value.resetFields()
  }
}

// 添加资源项
const addResourceItem = () => {
  if (!selectedResourceId.value) {
    ElMessage.warning('请选择资源')
    return
  }
  
  if (resourceQuantity.value <= 0) {
    ElMessage.warning('请输入有效的数量')
    return
  }
  
  // 查找选中的资源
  const resource = resourceList.value.find(r => r.id === selectedResourceId.value)
  if (!resource) {
    ElMessage.error('资源不存在')
    return
  }
  
  // 检查是否已添加该资源
  const existingItem = formData.items.find(item => item.resource_id === selectedResourceId.value)
  if (existingItem) {
    ElMessage.warning('该资源已添加到报价中')
    return
  }
  
  // 添加资源项
  formData.items.push({
    resource_id: resource.id,
    name: resource.name,
    unit: resource.unit,
    cost_price: resource.cost_price,
    sale_price: resource.sale_price,
    quantity: resourceQuantity.value,
    sub_total_cost: resource.cost_price * resourceQuantity.value,
    sub_total_sale: resource.sale_price * resourceQuantity.value
  })
  
  // 重置选择
  selectedResourceId.value = ''
  resourceQuantity.value = 1
  
  ElMessage.success('资源项添加成功')
}

// 移除资源项
const removeResourceItem = (index) => {
  formData.items.splice(index, 1)
  ElMessage.success('资源项移除成功')
}

// 保存报价
const saveQuotation = async () => {
  try {
    // 表单验证
    await quotationForm.value.validate()
    
    // 验证是否有资源项
    if (formData.items.length === 0) {
      ElMessage.warning('请至少添加一个资源项')
      return
    }
    
    // 准备提交数据
    const submitData = {
      project_name: formData.project_name,
      quote_date: formData.quote_date,
      items: formData.items.map(item => ({
        resource_id: item.resource_id,
        quantity: item.quantity
      }))
    }
    
    if (editingQuotation.value) {
      // 编辑报价
      await request.put(`/quotations/${editingQuotation.value.id}`, submitData)
      ElMessage.success('报价更新成功')
    } else {
      // 新增报价
      await request.post('/quotations', submitData)
      ElMessage.success('报价新增成功')
    }
    
    // 关闭对话框
    closeDialog()
    
    // 重新获取报价列表
    fetchQuotations()
  } catch (error) {
    if (error.name === 'Error') {
      ElMessage.error(error.message)
    } else {
      ElMessage.error('保存报价失败: ' + error.message)
    }
  }
}

// 删除报价
const deleteQuotation = async (quotationId) => {
  try {
    await ElMessageBox.confirm('确定要删除该报价吗？', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await request.delete(`/quotations/${quotationId}`)
    ElMessage.success('报价删除成功')
    
    // 重新获取报价列表
    fetchQuotations()
  } catch (error) {
    if (error.name !== 'ElMessageBoxCancel') {
      ElMessage.error('删除报价失败: ' + error.message)
    }
  }
}

// 查看报价明细
const viewQuotationItems = async (quotationId) => {
  try {
    const items = await request.get(`/quotations/${quotationId}/items`)
    quotationItems.value = items
    itemsDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取报价明细失败: ' + error.message)
  }
}

// 关闭报价明细对话框
const closeItemsDialog = () => {
  itemsDialogVisible.value = false
  quotationItems.value = []
}

// 分页相关方法
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchQuotations()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchQuotations()
}
</script>

<style scoped>
.quotation-view {
  padding: 0;
  height: 100%;
}

.quotation-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.dialog-footer {
  text-align: right;
}

.resource-item-selector {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.profit-positive {
  color: #67c23a;
  font-weight: bold;
}

.profit-negative {
  color: #f56c6c;
  font-weight: bold;
}
</style>
