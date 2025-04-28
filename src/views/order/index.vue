<script setup>
import { ElMessage } from 'element-plus';
import 'element-plus/theme-chalk/el-message.css';

const open2 = () => {
  ElMessage({
    showClose: true,
    message: 'Congrats, this is a success message.',
    type: 'success',
  })
}

</script>

<template>
  <div>订单</div>
  <el-button :plain="true" @click="open2">Success</el-button>
</template>

<style scoped>
</style>