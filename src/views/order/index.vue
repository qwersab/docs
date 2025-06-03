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
  <div class="order-list">
    <div class="order-card">
      <div class="order-header">
        <span>订单号 12233314</span>
      </div>
      <div class="order-body">
        <img class="order-img" src="https://img1.doubanio.com/view/subject/l/public/s29578632.jpg" alt="商品图片" />
        <div class="order-info">
          <div class="order-title">高数书 <span class="order-count">×3</span></div>
          <div class="order-detail">备注：请尽快发货</div>
          <div class="order-price">￥60.00</div>
          <div class="order-time">创建时间：2025-1-20 14:30:00</div>
          <el-button type="primary" size="small">确定退款</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.order-list {
  padding: 24px;
}
.order-card {
  border: 1px solid #eee;
  border-radius: 8px;
  margin-bottom: 24px;
  background: #fff;
  padding: 16px;
  max-width: 600px;
}
.order-header {
  font-size: 16px;
  color: #888;
  margin-bottom: 12px;
}
.order-body {
  display: flex;
  align-items: flex-start;
}
.order-img {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 4px;
  margin-right: 16px;
  border: 1px solid #eee;
}
.order-info {
  flex: 1;
}
.order-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 8px;
}
.order-count {
  color: #888;
  font-size: 14px;
  margin-left: 4px;
}
.order-detail {
  color: #666;
  margin-bottom: 8px;
}
.order-price {
  color: #e4393c;
  font-size: 20px;
  margin-bottom: 8px;
}
.order-time {
  color: #999;
  font-size: 14px;
  margin-bottom: 12px;
}
</style>