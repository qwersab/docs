<script setup>
import 'element-plus/theme-chalk/el-message.css';
</script>

<template>

  <RouterView />
</template>

<style scoped>
.custom-message {
  position: fixed !important;
  top: 10px !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  z-index: 1000 !important;
}
</style>
