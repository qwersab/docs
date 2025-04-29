<script setup lang="ts">
import { allProductStore } from '@/stores/allProductStore';
import { onMounted } from 'vue';
import productList from '@/components/productList.vue';
import { ref } from 'vue'
import type { TabsPaneContext } from 'element-plus'

const allproductStore=allProductStore()
const activeName = ref('all')
const minPrice = ref(0); // 默认最低价格
const maxPrice = ref(10000); // 默认最高价格
const isBargain = ref(false); // 是否支持砍价

onMounted(()=>{
  allproductStore.fetchProducts()
})

const applyFilter = () => {
  allproductStore.updateFilterConditions({
    minPrice: minPrice.value,
    maxPrice: maxPrice.value,
    isBargain: isBargain.value,
  });
};

const handleClick = (tab: TabsPaneContext) => {
  // 将 name 属性值从字符串转换为对应的数字
  const categoryMap = {
    all: undefined,
    books: 1,
    phones: 2,
    clothes: 3,
    others: 4
  };
  // const isBargainMap = {
  //   '全部': undefined,
  //   '支持砍价': true,
  //   '不支持砍价': false
  // };
  const categoryId = categoryMap[tab.paneName as keyof typeof categoryMap];
  // const bargain = isBargainMap[tab.paneName as keyof typeof isBargainMap];
  allproductStore.updateFilterConditions({ categoryId });
}

const handleClick2 = (tab: TabsPaneContext, event: Event) => {
  const isBargainMap = {
    '全部': undefined,
    '支持砍价': true,
    '不支持砍价': false
  };
  const bargain = isBargainMap[tab.paneName as keyof typeof isBargainMap];
  allproductStore.updateFilterConditions({ isBargain: bargain });
}


// 处理价格变化
const handlePriceChange = () => {
  // 确保最低价格小于等于最高价格
  if (minPrice.value > maxPrice.value) {
    minPrice.value = maxPrice.value;
  }
};

</script>

<template>
  <div class="header">
    <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
        <el-tab-pane label="全部" name="all"></el-tab-pane>
        <el-tab-pane label="书本" name="books"></el-tab-pane>
        <el-tab-pane label="手机" name="phones"></el-tab-pane>
        <el-tab-pane label="衣服" name="clothes"></el-tab-pane>
        <el-tab-pane label="其他" name="others"></el-tab-pane>
    </el-tabs>
    <el-tabs type="card" class="demo-tabs"  @tab-click="handleClick2">
      <el-tab-pane label="全部" name="全部"></el-tab-pane>
      <el-tab-pane label="支持砍价" name="支持砍价"></el-tab-pane>
      <el-tab-pane label="不支持砍价" name="不支持砍价"></el-tab-pane>
    </el-tabs>
    <div class="pricesel">
      <el-input-number
        v-model="minPrice"
        :min="0"
        :max="maxPrice"
        placeholder="最低价格"
        @change="handlePriceChange"
      />
      <el-input-number
        v-model="maxPrice"
        :min="minPrice"
        :max="10000"
        placeholder="最高价格"
        @change="handlePriceChange"
      />
      <el-button type="primary" @click="applyFilter">筛选</el-button>
    </div>
    
  </div>
  <div>
    <div v-if="allproductStore.filteredProducts.length>0" class="product-list">
      <productList
        v-for="product in allproductStore.filteredProducts"
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

<style scoped lang="less">
.header{
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  .pricesel{
    display: flex;
    gap:10px;
    .el-input-number {
      width: 130px; /* 设置输入框宽度 */
      height: 40px;
    }
  
  }
}
.product-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
.demo-tabs > .el-tabs__content {
  padding: 20px;
  color: #6b778c;
  font-weight: 600;
}


</style>