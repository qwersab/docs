<script setup>
import { useUserProductStore } from '@/stores/useProductStore';
import { onMounted } from 'vue';
import productList from '@/components/productList.vue';
const productStore=useUserProductStore()

onMounted(()=>{
  productStore.fetchProducts()
})

</script>

<template>
  <div>
    <div v-if="productStore.products.length > 0" class="product-list">
      <productList
        v-for="product in productStore.products"
        :key="product.id"
        :product="product"
        :show-actions="true"
      />
      
    </div>
    <div v-else>
      <p>暂无商品</p>
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