<script setup>
import { ref, onMounted } from 'vue';
import { getfootprint } from '@/api';
import productList from '@/components/productList.vue';

const lookProducts = ref([]);
const isLoading = ref(false);

const fetchFootprint = async () => {
  isLoading.value = true;
  try {
    const response = await getfootprint();
    lookProducts.value = response.data;
  } catch (error) {
    console.error('获取浏览商品失败', error);
    lookProducts.value = [];
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchFootprint();
});
</script>

<template>
  <div>
    <h2>我的足迹</h2>
    <div v-if="isLoading">加载中...</div>
    <div v-else>
      <div v-if="lookProducts.length > 0" class="product-list">
        <productList
          v-for="product in lookProducts"
          :key="product.id"
          :product="product"
          :show-actions="false"
        />
      </div>
      <div v-else>
        <p>暂无浏览记录</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.product-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
</style>