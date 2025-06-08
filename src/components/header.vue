<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import {getuser} from '../api/index'
import { ElMessage } from 'element-plus';

const router=useRouter()


const isLoggedIn = localStorage.getItem('tr_token')?true:false; // 假设用户已经登录，可以根据实际情况动态设置
const input = ref(''); // 搜索框的绑定值

// 用户信息
const userInfo = ref({
  avatar: 'https://example.com/avatar.jpg', // 用户头像链接
  name: '张三', // 用户姓名
  viewCount: 120, // 商品被浏览数
  favoriteCount: 50, // 商品被收藏数
  wantCount: 30 // 商品被想要数
});


const items = ref([
  { type: 'warning', label: `商品被浏览${userInfo.value.viewCount}` },
  { type: 'warning', label: `商品被收藏${userInfo.value.favoriteCount}` },
  { type: 'warning', label: `商品被想要${userInfo.value.wantCount}` },
  
])

onMounted(()=>{
  const getUserInfo=async ()=>{
    const {data}=await getuser()
    userInfo.value.avatar=data.profile_picture
    userInfo.value.name=data.username
  }

  getUserInfo()
})

//路由跳转
const handleSelect = (index) => {
  switch (index) {
    case '0':
      router.push('/'); // 跳转到首页
      break;
    case '1':
      router.push('/allproduct'); // 跳转到商品页面
      break;
    case '2':
      router.push('/myproduct'); // 跳转到我的商品页面
      break;
    case '3':
      router.push('/collection'); // 跳转到我的收藏页面
      break;
    case '4':
      router.push('/footprints'); // 跳转到足迹页面
      break;
    case '5':
      router.push('/order'); // 跳转到订单页面
      break;
    // case '6':
    //   router.push('/notice'); // 跳转到通知页面
    //   break;
    case '7':
      router.push('/submitproduct'); // 跳转到发布商品页面
      break;
    case '8-1':
      router.push('/login'); // 跳转到登录页面
      break;
    case 'login':
      router.push('/login'); // 跳转到登录页面
      break;
    case 'register':
      router.push('/register'); // 跳转到登录页面
      break;
    default:
      console.log('未知的菜单项');
  }
}

const handleSearch = () => {
  if (!input.value.trim()) {
    ElMessage.warning('请输入搜索内容');
    return;
  }
  router.push({ path: '/allproduct', query: { keyword: input.value.trim() } });
};
</script>

<template>
  <div style="display: flex; justify-content: space-between; height: auto; background-color: #545c64; color: white;">
    <!-- 左侧菜单 -->
    <div style="flex: 1; display: flex; flex-direction: column;">
      <el-menu
        :default-active="activeIndex"
        class="el-menu-demo"
        mode="horizontal"
        @select="handleSelect"
        background-color="#545c64"
        text-color="white"
        style="flex: 1;"
      >
        <el-menu-item index="0">
          <img
            style="width: 50px"
            src="../images/shopping.svg"
            alt="Element logo"
          />
          <div style="font-size: 16px;">校园二手交易平台</div>
        </el-menu-item>
        <template v-if="isLoggedIn">
          <el-menu-item index="1">商品</el-menu-item>
          <el-menu-item index="2">我的商品</el-menu-item>
          <el-menu-item index="3">我的收藏</el-menu-item>
          <el-menu-item index="4">足迹</el-menu-item>
        </template>
        <template v-else>
          <el-menu-item index="login">登录</el-menu-item>
          <el-menu-item index="register">注册</el-menu-item>
        </template>
      </el-menu>

      <!-- 用户信息（登录后显示） -->
      <div v-if="isLoggedIn" style="display: flex; align-items: center; padding: 10px; background-color: #545c64; color: white;">
        <router-link to="/mine" style="display: flex; align-items: center;">
          <el-avatar :size="40" :src="userInfo.avatar" />
        </router-link>
        
        <div style="margin-left: 10px;">
            <div>{{ userInfo.name }}</div>
            <div class="flex gap-2">
              <el-tag
                v-for="item in items"
                :key="item.label"
                :type="item.type"
                effect="dark"
                round
              >
                {{ item.label }}
              </el-tag>
            </div>

        </div>
        
      </div>
    </div>

    <!-- 右侧菜单 -->
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
      background-color="#545c64"
      text-color="white"
      style="flex: 1; justify-content: flex-end;"
    >
      <template v-if="isLoggedIn">
        <el-input v-model="input" style="width: 150px; height: 30px; line-height: height;" placeholder="请输入要搜索的商品" @keyup.enter="handleSearch" />
        <el-menu-item index="5">订单</el-menu-item>
        <!-- <el-menu-item index="6">通知</el-menu-item> -->
        <el-menu-item index="7">发布商品</el-menu-item>
        <el-sub-menu index="8">
          <template #title>
            <el-avatar :src="userInfo.avatar || 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'" />
          </template>
          <el-menu-item index="8-1">退出</el-menu-item>
        </el-sub-menu>
      </template>
    </el-menu>
  </div>
</template>

<style scoped lang="less">
.el-menu-demo {
  width: 100%;
  background-color: #545c64;
  color: white;
}

.el-menu-item {
  margin: 0 5px; /* 添加菜单项之间的间距 */
  font-size: 12px;
}

.el-avatar {
  margin-right: 10px; /* 添加头像和用户信息之间的间距 */
}
</style>