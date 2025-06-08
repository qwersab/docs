<script setup>
import { ref, onMounted } from 'vue';
import { getbuyorder, getsellorder } from '@/api/index.js';
import { ElMessage } from 'element-plus';
import 'element-plus/theme-chalk/el-message.css';
import order from '@/components/order.vue';

const activeName = ref('first');
const buyOrders = ref([]);
const sellOrders = ref([]);
const loading = ref(false);

const fetchOrders = async () => {
  loading.value = true;
  try {
    const [buyRes, sellRes] = await Promise.all([
      getbuyorder(),
      getsellorder()
    ]);
    buyOrders.value = buyRes.data || [];
    sellOrders.value = sellRes.data || [];
  } catch (e) {
    ElMessage.error('订单获取失败');
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchOrders();
});

const handleClick = () => {};
</script>

<template>
    <el-tabs
    v-model="activeName"
    type="card"
    class="demo-tabs"
    @tab-click="handleClick"
  >
    <el-tab-pane label="购物订单" name="first">
      <order :orders="buyOrders" :loading="loading" userType="buyer" @refresh="fetchOrders" />
    </el-tab-pane>
    <el-tab-pane label="卖出订单" name="second">
      <order :orders="sellOrders" :loading="loading" userType="seller" @refresh="fetchOrders" />
    </el-tab-pane>
  </el-tabs>
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