<template>
  <div class="resource-view">
    <el-card class="resource-card">
      <template #header>
        <div class="card-header">
          <span>资源管理</span>
          <el-button type="primary" @click="openAddDialog">
            <el-icon><Plus /></el-icon>
            新增资源
          </el-button>
        </div>
      </template>
      
      <!-- 资源列表 -->
      <el-table :data="resourceList" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="remark" label="备注" />
        <el-table-column prop="unit" label="单位" width="100" />
        <el-table-column prop="cost_price" label="成本价" width="120">
          <template #default="{ row }">
            {{ row.cost_price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="sale_price" label="销售价" width="120">
          <template #default="{ row }">
            {{ row.sale_price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="openEditDialog(row)">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteResource(row.id)">
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
    
    <!-- 新增/编辑资源对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      @close="closeDialog"
    >
      <el-form
        ref="resourceForm"
        :model="formData"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入资源名称" />
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="formData.remark" placeholder="请输入备注" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="单位" prop="unit">
          <el-input v-model="formData.unit" placeholder="请输入单位" />
        </el-form-item>
        <el-form-item label="成本价" prop="cost_price">
          <el-input v-model.number="formData.cost_price" placeholder="请输入成本价" />
        </el-form-item>
        <el-form-item label="销售价" prop="sale_price">
          <el-input v-model.number="formData.sale_price" placeholder="请输入销售价" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closeDialog">取消</el-button>
          <el-button type="primary" @click="saveResource">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import request from '../utils/request'

// 响应式数据
const resourceList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 对话框相关
const dialogVisible = ref(false)
const dialogTitle = ref('新增资源')
const editingResource = ref(null)

// 表单引用
const resourceForm = ref(null)

// 表单数据
const formData = reactive({
  name: '',
  remark: '',
  unit: '',
  cost_price: 0,
  sale_price: 0
})

// 表单验证规则
const formRules = reactive({
  name: [
    { required: true, message: '请输入资源名称', trigger: 'blur' }
  ],
  unit: [
    { required: true, message: '请输入单位', trigger: 'blur' }
  ],
  cost_price: [
    { required: true, message: '请输入成本价', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '成本价必须大于0', trigger: 'blur' }
  ],
  sale_price: [
    { required: true, message: '请输入销售价', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '销售价必须大于0', trigger: 'blur' }
  ]
})

// 生命周期钩子
onMounted(() => {
  fetchResources()
})

// 获取资源列表
const fetchResources = async () => {
  try {
    const data = await request.get('/resources')
    resourceList.value = data
    total.value = data.length
  } catch (error) {
    ElMessage.error('获取资源列表失败: ' + error.message)
  }
}

// 打开新增对话框
const openAddDialog = () => {
  dialogTitle.value = '新增资源'
  editingResource.value = null
  resetForm()
  dialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (resource) => {
  dialogTitle.value = '编辑资源'
  editingResource.value = resource
  
  // 填充表单数据
  formData.name = resource.name
  formData.remark = resource.remark || ''
  formData.unit = resource.unit
  formData.cost_price = resource.cost_price
  formData.sale_price = resource.sale_price
  
  dialogVisible.value = true
}

// 关闭对话框
const closeDialog = () => {
  dialogVisible.value = false
  resetForm()
}

// 重置表单
const resetForm = () => {
  formData.name = ''
  formData.remark = ''
  formData.unit = ''
  formData.cost_price = 0
  formData.sale_price = 0
  
  // 重置表单验证
  if (resourceForm.value) {
    resourceForm.value.resetFields()
  }
}

// 保存资源
const saveResource = async () => {
  try {
    // 表单验证
    await resourceForm.value.validate()
    
    if (editingResource.value) {
      // 编辑资源
      await request.put(`/resources/${editingResource.value.id}`, formData)
      ElMessage.success('资源更新成功')
    } else {
      // 新增资源
      await request.post('/resources', formData)
      ElMessage.success('资源新增成功')
    }
    
    // 关闭对话框
    closeDialog()
    
    // 重新获取资源列表
    fetchResources()
  } catch (error) {
    if (error.name === 'Error') {
      ElMessage.error(error.message)
    } else {
      ElMessage.error('保存资源失败: ' + error.message)
    }
  }
}

// 删除资源
const deleteResource = async (resourceId) => {
  try {
    await ElMessageBox.confirm('确定要删除该资源吗？', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await request.delete(`/resources/${resourceId}`)
    ElMessage.success('资源删除成功')
    
    // 重新获取资源列表
    fetchResources()
  } catch (error) {
    if (error.name !== 'ElMessageBoxCancel') {
      ElMessage.error('删除资源失败: ' + error.message)
    }
  }
}

// 分页相关方法
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchResources()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchResources()
}
</script>

<style scoped>
.resource-view {
  padding: 0;
  height: 100%;
}

.resource-card {
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
</style>
