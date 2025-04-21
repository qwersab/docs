<script setup>
import Header from '../components/header.vue'
</script>

<template>
  <div class="common-layout">
    <el-container class="layout-container">
      <el-header class="layout-header">
        <Header />
      </el-header>
      <el-main class="layout-main">
        <RouterView />
      </el-main>
    </el-container>
  </div>
</template>

<style scoped>
.common-layout {
  height: 100vh; /* 确保布局占满整个视口高度 */
  display: flex;
}

.layout-container {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.layout-header {
  height: auto; /* 让Header组件决定高度 */
  padding: 0; /* 移除默认padding，让Header完全控制 */
}

.layout-main {
  flex: 1;
  padding: 20px; /* 可根据需要调整 */
  overflow: auto; /* 内容超出时显示滚动条 */
}

/* 响应式设计 - 可选 */
@media (max-width: 768px) {
  .layout-main {
    padding: 10px;
  }
}
</style>