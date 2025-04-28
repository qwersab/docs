<script setup>
import { allProductStore } from '@/stores/allProductStore';
import { onMounted } from 'vue';
import productList from '@/components/productList.vue';
const allproductStore=allProductStore()

onMounted(()=>{
  allproductStore.fetchProducts()
})

</script>

<template>
  <div>
    
  </div>
  <div>
    <div v-if="allproductStore.products.length > 0" class="product-list">
      <productList
        v-for="product in allproductStore.products"
        :key="product.id"
        :product="product"
        :show-actions="false"
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