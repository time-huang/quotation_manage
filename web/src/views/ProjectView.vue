<template>
  <div class="project-view">
    <el-card class="project-card">
      <template #header>
        <div class="card-header">
          <span>项目管理</span>
          <el-button type="primary" @click="openAddDialog">
            <el-icon><Plus /></el-icon>
            新增项目
          </el-button>
        </div>
      </template>
      
      <!-- 项目列表 -->
      <el-table :data="projectList" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="项目名称" />
        <el-table-column prop="project_date" label="项目日期" width="150" />
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewProjectDetails(row.id)">
              <el-icon><View /></el-icon>
              查看详情
            </el-button>
            <el-button type="warning" size="small" @click="openEditDialog(row)">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteProject(row.id)">
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
    
    <!-- 新增/编辑项目对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="800px"
      @close="closeDialog"
    >
      <el-form
        ref="projectForm"
        :model="formData"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="项目日期" prop="project_date">
          <el-date-picker
            v-model="formData.project_date"
            type="date"
            placeholder="请选择项目日期"
            style="width: 100%"
          />
        </el-form-item>
        
        <!-- 分组和资源配置 -->
        <el-form-item label="项目分组">
          <div class="group-configurator">
            <!-- 新增分组 -->
            <div class="add-group">
              <el-input
                v-model="newGroupName"
                placeholder="请输入分组名称"
                style="width: 200px; margin-right: 10px"
              />
              <el-button type="primary" @click="addGroup">
                <el-icon><Plus /></el-icon>
                新增分组
              </el-button>
            </div>
            
            <!-- 分组列表 -->
            <div class="group-list">
              <el-collapse v-model="activeGroupNames">
                <el-collapse-item
                  v-for="(group, groupIndex) in formData.groups"
                  :key="groupIndex"
                  :title="group.name"
                  :name="group.name"
                >
                  <div class="group-content">
                    <!-- 资源选择 -->
                    <div class="resource-selector">
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
                      <el-button type="primary" @click="addResourceToGroup(groupIndex)">
                        <el-icon><Plus /></el-icon>
                        添加资源
                      </el-button>
                    </div>
                    
                    <!-- 已选择的资源 -->
                    <el-table :data="group.resources" style="width: 100%; margin-top: 10px" border>
                      <el-table-column prop="name" label="资源名称" />
                      <el-table-column prop="unit" label="单位" width="100" />
                      <el-table-column prop="quantity" label="数量" width="100" />
                      <el-table-column label="操作" width="100">
                        <template #default="{ row, $index }">
                          <el-button type="danger" size="small" @click="removeResourceFromGroup(groupIndex, $index)">
                            <el-icon><Delete /></el-icon>
                            删除
                          </el-button>
                        </template>
                      </el-table-column>
                    </el-table>
                    
                    <!-- 删除分组按钮 -->
                    <div style="margin-top: 10px; text-align: right">
                      <el-button type="danger" size="small" @click="removeGroup(groupIndex)">
                        <el-icon><Delete /></el-icon>
                        删除分组
                      </el-button>
                    </div>
                  </div>
                </el-collapse-item>
              </el-collapse>
            </div>
          </div>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closeDialog">取消</el-button>
          <el-button type="primary" @click="saveProject">保存</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 项目详情对话框 -->
    <el-dialog
      v-model="detailsDialogVisible"
      title="项目详情"
      width="800px"
      @close="closeDetailsDialog"
    >
      <el-form
        :model="detailsData"
        label-width="100px"
      >
        <el-form-item label="项目名称">
          <el-input v-model="detailsData.name" disabled />
        </el-form-item>
        <el-form-item label="项目日期">
          <el-input v-model="detailsData.project_date" disabled />
        </el-form-item>
        
        <!-- 分组和资源详情 -->
        <el-form-item label="项目分组">
          <div class="group-details">
            <el-collapse v-model="activeDetailsGroupNames">
              <el-collapse-item
                v-for="(group, groupIndex) in detailsData.groups"
                :key="groupIndex"
                :title="group.name"
                :name="group.name"
              >
                <div class="group-content">
                  <el-table :data="group.resources" style="width: 100%" border>
                    <el-table-column prop="name" label="资源名称" />
                    <el-table-column prop="unit" label="单位" width="100" />
                    <el-table-column prop="quantity" label="数量" width="100" />
                  </el-table>
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Edit, Delete, View } from '@element-plus/icons-vue'
import { getProjects, getProject, createProject, updateProject, deleteProject as deleteProjectAPI, getResources } from '../utils/api'

// 数据
const projectList = ref([])
const resourceList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 对话框
const dialogVisible = ref(false)
const detailsDialogVisible = ref(false)
const dialogTitle = ref('新增项目')

// 表单数据
const formData = reactive({
  id: null,
  name: '',
  project_date: '',
  groups: []
})

const detailsData = reactive({
  id: null,
  name: '',
  project_date: '',
  groups: []
})

// 表单规则
const formRules = reactive({
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' }
  ],
  project_date: [
    { required: true, message: '请选择项目日期', trigger: 'change' }
  ]
})

// 临时数据
const newGroupName = ref('')
const selectedResourceId = ref(null)
const resourceQuantity = ref(1)
const activeGroupNames = ref([])
const activeDetailsGroupNames = ref([])

// 生命周期
onMounted(() => {
  loadProjects()
  loadResources()
})

// 加载项目列表
const loadProjects = async () => {
  try {
    console.log('开始获取最新项目列表')
    const response = await getProjects()
    console.log('获取到的最新项目列表:', response)
    projectList.value = response
    total.value = response.length
  } catch (error) {
    ElMessage.error('加载项目列表失败')
    console.error(error)
  }
}

// 加载资源列表
const loadResources = async () => {
  try {
    const response = await getResources()
    resourceList.value = response
  } catch (error) {
    ElMessage.error('加载资源列表失败')
    console.error(error)
  }
}

// 打开新增对话框
const openAddDialog = () => {
  dialogTitle.value = '新增项目'
  formData.id = null
  formData.name = ''
  formData.project_date = ''
  formData.groups = []
  newGroupName.value = ''
  selectedResourceId.value = null
  resourceQuantity.value = 1
  activeGroupNames.value = []
  dialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = async (row) => {
  dialogTitle.value = '编辑项目'
  try {
    const project = await getProject(row.id)
    formData.id = project.id
    formData.name = project.name
    formData.project_date = project.project_date
    formData.groups = project.groups || []
    activeGroupNames.value = formData.groups.map(group => group.name)
    dialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取项目详情失败')
    console.error(error)
  }
}

// 打开详情对话框
const viewProjectDetails = async (projectId) => {
  try {
    const project = await getProject(projectId)
    detailsData.id = project.id
    detailsData.name = project.name
    detailsData.project_date = project.project_date
    detailsData.groups = project.groups || []
    activeDetailsGroupNames.value = detailsData.groups.map(group => group.name)
    detailsDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取项目详情失败')
    console.error(error)
  }
}

// 关闭对话框
const closeDialog = () => {
  dialogVisible.value = false
  newGroupName.value = ''
  selectedResourceId.value = null
  resourceQuantity.value = 1
  activeGroupNames.value = []
}

// 关闭详情对话框
const closeDetailsDialog = () => {
  detailsDialogVisible.value = false
  activeDetailsGroupNames.value = []
}

// 新增分组
const addGroup = () => {
  if (!newGroupName.value.trim()) {
    ElMessage.warning('请输入分组名称')
    return
  }
  
  // 检查分组名称是否已存在
  const existingGroup = formData.groups.find(group => group.name === newGroupName.value.trim())
  if (existingGroup) {
    ElMessage.warning('分组名称已存在')
    return
  }
  
  formData.groups.push({
    name: newGroupName.value.trim(),
    resources: []
  })
  
  activeGroupNames.value.push(newGroupName.value.trim())
  newGroupName.value = ''
}

// 删除分组
const removeGroup = (groupIndex) => {
  if (formData.groups[groupIndex].resources.length > 0) {
    ElMessage.warning('请先删除分组中的所有资源')
    return
  }
  
  activeGroupNames.value.splice(activeGroupNames.value.indexOf(formData.groups[groupIndex].name), 1)
  formData.groups.splice(groupIndex, 1)
}

// 添加资源到分组
const addResourceToGroup = (groupIndex) => {
  if (!selectedResourceId.value) {
    ElMessage.warning('请选择资源')
    return
  }
  
  if (resourceQuantity.value <= 0) {
    ElMessage.warning('请输入有效的数量')
    return
  }
  
  const resource = resourceList.value.find(r => r.id === selectedResourceId.value)
  if (!resource) {
    ElMessage.warning('资源不存在')
    return
  }
  
  // 检查资源是否已存在于分组中
  const existingResource = formData.groups[groupIndex].resources.find(r => r.resource_id === selectedResourceId.value)
  if (existingResource) {
    ElMessage.warning('资源已存在于该分组中')
    return
  }
  
  formData.groups[groupIndex].resources.push({
    resource_id: selectedResourceId.value,
    name: resource.name,
    unit: resource.unit,
    quantity: resourceQuantity.value
  })
  
  selectedResourceId.value = null
  resourceQuantity.value = 1
}

// 从分组中删除资源
const removeResourceFromGroup = (groupIndex, resourceIndex) => {
  formData.groups[groupIndex].resources.splice(resourceIndex, 1)
}

// 表单引用
const projectForm = ref(null)

// 保存项目
const saveProject = async () => {
  try {
    // 验证表单
    const valid = await projectForm.value.validate()
    if (!valid) {
      return
    }
    
    let response
    if (formData.id) {
      // 编辑项目
      response = await updateProject(formData.id, formData)
    } else {
      // 新增项目
      response = await createProject(formData)
    }
    
    // 保存成功，因为响应拦截器只在成功时返回数据
    ElMessage.success(formData.id ? '项目更新成功' : '项目创建成功')
    closeDialog()
    loadProjects()
  } catch (error) {
    ElMessage.error('保存项目失败')
    console.error(error)
  }
}

// 删除项目
const deleteProject = async (projectId) => {
  try {
    await deleteProjectAPI(projectId)
    ElMessage.success('项目删除成功')
    console.log('调用loadProjects函数获取最新项目列表')
    loadProjects()
  } catch (error) {
    ElMessage.error('项目删除失败')
    console.error(error)
  }
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  loadProjects()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  loadProjects()
}
</script>

<style scoped>
.project-view {
  padding: 20px;
}

.project-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.group-configurator {
  margin-top: 10px;
}

.add-group {
  margin-bottom: 20px;
}

.group-list {
  max-height: 400px;
  overflow-y: auto;
}

.group-content {
  padding: 10px;
}

.resource-selector {
  margin-bottom: 10px;
}

.group-details {
  max-height: 400px;
  overflow-y: auto;
}
</style>