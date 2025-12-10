<script setup>
import { RouterView } from 'vue-router'
import { Menu as MenuIcon, Document as DocumentIcon } from '@element-plus/icons-vue'
</script>

<template>
  <div class="app-container">
    <!-- 侧边栏导航 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>报价管理系统</h2>
      </div>
      <nav class="sidebar-nav">
        <el-menu
          :default-active="$route.path"
          class="el-menu-vertical-demo"
          router
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
}

.sidebar-header {
  padding: 20px;
  background-color: #263445;
  border-bottom: 1px solid #1f2d3d;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
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
