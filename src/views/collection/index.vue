<script setup>
import { ref, onMounted } from 'vue';
import { getcollection } from '@/api';
import productList from '@/components/productList.vue';

const collectionProducts = ref([]);
const isLoading = ref(false);

const fetchCollection = async () => {
  isLoading.value = true;
  try {
    const response = await getcollection();
    collectionProducts.value = response.data;
  } catch (error) {
    console.error('获取收藏商品失败', error);
    collectionProducts.value = [];
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchCollection();
});
</script>

<template>
  <div>
    <h2>我的收藏</h2>
    <div v-if="isLoading">加载中...</div>
    <div v-else>
      <div v-if="collectionProducts.length > 0" class="product-list">
        <productList
          v-for="product in collectionProducts"
          :key="product.id"
          :product="product"
          :show-actions="false"
        />
      </div>
      <div v-else>
        <p>暂无收藏商品</p>
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