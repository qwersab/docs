<!-- <script setup>
import {ref} from 'vue'
const props=defineProps({
  product:{
    type:Object,
    required:true
  },
  showActions:{
    type:Boolean,
    default:false
  }
})

//互动行为初始状态
const product=ref({
  ...props.product,
  wantsCount:0,
  isCollected:false,
  isViewed:false
})

// 解析 cover_list 字符串，提取第一张图片的 URL
const getFirstImageUrl = (cover_list) => {
  // 如果 cover_list 为空或 undefined，返回默认图片
  if (!cover_list) {
    return 'https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png';
  }

  // 直接返回 cover_list，因为它已经是一个图片链接
  return cover_list;
};
</script>

<template>
   <el-card style="max-width: 450px;">
    <img 
    :src="getFirstImageUrl(props.product.cover_list)" 
    alt=""
    style="width: 100%;height: 250px; object-fit: cover;" />
    <template #footer>
      <el-tag
      effect="light"
      round
      :type="product.is_bargain ? 'success' : 'info'"
      >
        {{ product.is_bargain ? '支持砍价' : '不支持砍价' }}
      </el-tag>
      <span class="product-name">{{ product.name }}</span>
      <div class="product-price">￥ {{ product.price }}</div>
      <span class="product-wants">{{ product.wantsCount }} 人想要</span>
      <div v-if="showActions" class="actions">
        <el-button type="primary">编辑</el-button>
        <el-button>删除</el-button>
      </div>
    </template>
  </el-card>
</template>

<style scoped>
.product-name {
  font-size: 16px;
  font-weight: bold;
  margin: 10px 0;
}

.product-price {
  font-size: 18px;
  color: #f56c6c;
  margin: 5px 0;
}

.product-wants {
  font-size: 14px;
  color: #909399;
}
</style> -->

<script setup>
import { ref } from 'vue';

const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
  showActions: {
    type: Boolean,
    default: false,
  },
});

// 互动行为初始状态
const product = ref({
  ...props.product,
  wantsCount: 0,
  isCollected: false,
  isViewed: false,
});

// 解析 cover_list 字符串，提取第一张图片的 URL
const getFirstImageUrl = (cover_list) => {
  // 如果 cover_list 为空或 undefined，返回默认图片
  if (!cover_list) {
    console.warn('No cover_list provided. Using default image.');
    return 'https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png';
  }
  const urls = cover_list.split(',');
  const firstUrl = urls[0].trim();

  // 直接返回 cover_list，因为它已经是一个图片链接
  return firstUrl;
};
</script>

<template>
  <el-card class="product-card">
    <img
      :src="getFirstImageUrl(product.cover_list)"
      alt=""
      class="responsive-image"
    />
    <template #footer>
      <el-tag
        effect="light"
        round
        :type="product.is_bargain ? 'success' : 'info'"
      >
        {{ product.is_bargain ? '支持砍价' : '不支持砍价' }}
      </el-tag>
      <span class="product-name">{{ product.name }}</span>
      <div class="product-price">￥ {{ product.price }}</div>
      <span class="product-wants">{{ product.wantsCount }} 人想要</span>
      <!-- 条件渲染操作按钮 -->
      <div v-if="showActions" class="actions">
        <el-button type="primary">编辑</el-button>
        <el-button>删除</el-button>
      </div>
    </template>
  </el-card>
</template>

<style scoped>
.product-card {
  width: 320px;
  height: 450px; /* 固定卡片高度 */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.responsive-image {
  width: 100%;
  height: 250px; /* 固定图片高度 */
  object-fit: cover; /* 裁剪图片以适应容器 */
}

.product-name {
  font-size: 16px;
  font-weight: bold;
  margin: 10px 0;
}

.product-price {
  font-size: 18px;
  color: #f56c6c;
  margin: 5px 0;
}

.product-wants {
  font-size: 14px;
  color: #909399;
}

.actions {
  display: flex;
  justify-content: space-between;
}
</style>