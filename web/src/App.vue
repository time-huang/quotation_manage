<script setup>
import { RouterView } from 'vue-router'
import { ref } from 'vue'
import { Menu as MenuIcon, Document as DocumentIcon, Expand as ExpandIcon, Fold as FoldIcon } from '@element-plus/icons-vue'

// 控制菜单收起/展开状态
const isCollapse = ref(false)
</script>

<template>
  <div class="app-container">
    <!-- 侧边栏导航 -->
    <aside class="sidebar" :class="{ 'sidebar-collapsed': isCollapse }">
      <div class="sidebar-header">
        <h2 v-if="!isCollapse">报价管理系统</h2>
        <el-icon v-else><MenuIcon /></el-icon>
        <el-button
          class="collapse-btn"
          type="text"
          @click="isCollapse = !isCollapse"
        >
          <el-icon><ExpandIcon v-if="isCollapse" /><FoldIcon v-else /></el-icon>
        </el-button>
      </div>
      <nav class="sidebar-nav">
        <el-menu
          :default-active="$route.path"
          class="el-menu-vertical-demo"
          router
          :collapse="isCollapse"
          :collapse-transition="false"
        >
          <el-menu-item index="/">
            <el-icon><MenuIcon /></el-icon>
            <span>资源管理</span>
          </el-menu-item>
          <el-menu-item index="/quotation">
            <el-icon><DocumentIcon /></el-icon>
            <span>报价管理</span>
          </el-menu-item>
        </el-menu>
      </nav>
    </aside>
    
    <!-- 主内容区域 -->
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 250px;
  background-color: #304156;
  color: #fff;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
}

.sidebar-collapsed {
  width: 64px;
}

.sidebar-header {
  padding: 20px;
  background-color: #263445;
  border-bottom: 1px solid #1f2d3d;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.collapse-btn {
  color: #fff;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-nav {
  flex: 1;
  padding: 10px 0;
}

.el-menu-vertical-demo {
  background-color: transparent;
  border-right: none;
}

.el-menu-item {
  color: #bfcbd9;
  border-bottom: 1px solid #1f2d3d;
}

.el-menu-item:hover {
  background-color: #263445;
  color: #fff;
}

.el-menu-item.is-active {
  background-color: #1890ff;
  color: #fff;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  background-color: #f5f7fa;
}
</style>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

#app {
  height: 100vh;
}
</style>
