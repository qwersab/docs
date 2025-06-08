<script setup>
import { defineProps, defineEmits } from 'vue';
import { ElMessage, ElButton, ElEmpty, ElSkeleton, ElPopconfirm } from 'element-plus';
import 'element-plus/theme-chalk/el-message.css';
import { postRefund, postReviewRefund, postReviewOrder } from '@/api/index.js';

const props = defineProps({
  orders: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  userType: {
    type: String,
    default: 'buyer'
  }
});

const emits = defineEmits(['refresh']);

const applyRefund = async (order) => {
  try {
    await postRefund({ order_id: order.id });
    ElMessage.success('已提交退款申请');
    emits('refresh');
  } catch (e) {
    ElMessage.error(e?.response?.data?.error || '申请退款失败');
  }
};

const reviewRefund = async (order, is_approved) => {
  try {
    await postReviewRefund({ order_id: order.id, is_approved });
    ElMessage.success(is_approved ? '已同意退款' : '已拒绝退款');
    emits('refresh');
  } catch (e) {
    ElMessage.error(e?.response?.data?.error || '操作失败');
  }
};

const reviewOrder = async (order, is_approved) => {
  try {
    await postReviewOrder({ order_id: order.id, is_approved });
    ElMessage.success(is_approved ? '已同意交易' : '已拒绝交易');
    emits('refresh');
  } catch (e) {
    ElMessage.error(e?.response?.data?.error || '操作失败');
  }
};
</script>

<template>
  <div class="order-list">
    <el-skeleton :loading="loading" animated :count="2">
      <template #template>
        <div class="order-card">
          <div class="order-header">
            <span>订单号 加载中...</span>
          </div>
          <div class="order-body">
            <el-skeleton-item variant="image" class="order-img" />
            <div class="order-info">
              <div class="order-title">商品名 <span class="order-count">×--</span></div>
              <div class="order-detail">备注：--</div>
              <div class="order-price">￥--</div>
              <div class="order-time">创建时间：--</div>
              <el-button type="primary" size="small" disabled>申请退款</el-button>
            </div>
          </div>
        </div>
      </template>
      <template #default>
        <template v-if="orders.length">
          <div class="order-card" v-for="order in orders" :key="order.id">
            <div class="order-header">
              <span>订单号 {{ order.code }}</span>
              <span style="float:right; color:#409EFF;">{{ order.trade_status_display }}</span>
            </div>
            <div class="order-body">
              <img class="order-img" :src="order.product_info.cover_list || 'https://img1.doubanio.com/view/subject/l/public/s29578632.jpg'" alt="商品图片" />
              <div class="order-info">
                <div class="order-title">{{ order.product_info.name }} <span class="order-count">×1</span></div>
                <div class="order-detail">{{ order.detail }}</div>
                <div class="order-price">￥{{ order.buy_price }}</div>
                <div class="order-time">创建时间：{{ order.create_time ? order.create_time.replace('T', ' ').slice(0, 19) : '--' }}</div>
                <!-- 买家视角 -->
                <template v-if="props.userType === 'buyer'">
                  <el-button
                    v-if="order.trade_status === 1"
                    type="primary"
                    size="small"
                    @click="applyRefund(order)"
                  >申请退款</el-button>
                  <span v-else-if="order.trade_status === 3">退款处理中</span>
                  <span v-else-if="order.trade_status === 4">已退款</span>
                </template>
                <!-- 卖家视角 -->
                <template v-else-if="props.userType === 'seller'">
                  <template v-if="order.trade_status === 0">
                    <div title="确定同意交易？" @click="reviewOrder(order, true)">
                      <el-button type="success" size="small">同意交易</el-button>
                    </div>
                    <div title="确定拒绝交易？" @click="reviewOrder(order, false)">
                      <el-button type="danger" size="small">拒绝交易</el-button>
                    </div>
                  </template>
                  <template v-else-if="order.trade_status === 3">
                    <div title="确定同意退款？" @click="reviewRefund(order, true)">
                      <el-button type="success" size="small">同意退款</el-button>
                    </div>
                    <div title="确定拒绝退款？" @click="reviewRefund(order, false)">
                      <el-button type="danger" size="small">拒绝退款</el-button>
                    </div>
                  </template>
                  <span v-else-if="order.trade_status === 4">已退款</span>
                </template>
              </div>
            </div>
          </div>
        </template>
        <div v-else>暂无订单</div>
      </template>
    </el-skeleton>
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