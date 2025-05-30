<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { getproductbyid ,getuseradd,getuser,getinteraction,getprointeraction} from '@/api';
import { useRoute } from 'vue-router';
// 浏览1 收藏2 想要3
interface Product{
  id: number,
  name: string,
  category_id: number,
  category_name: string,
  cover_list: Array<string>,
  detail: string,
  inventory: number,
  is_bargain: boolean,
  old_level: number,
  price: number,
  user_id: number,
}

interface Publisher {
  id:number,
  username:string
  profile_picture: string;
}

interface Mine{
  id:number,
  username:string,
  profile_picture: string;
}

interface Interaction{
  product_id: number,
  want_count: number,
  browse_count: number,
  favorite_count: number
}

const route = useRoute();
const product = ref<Product | null>(null);
const coverListarr = ref<string[]>([]);
const pubulisher=ref<Publisher|null>(null)
const me=ref<Mine|null>(null)
const textarea = ref('')
const dialogVisible = ref(false)
const num = ref(1)
const interaction=ref<Interaction|null>(null)
const comments = ref([
  {
    id: 1,
    user: {
      username: '用户1',
      profile_picture: 'https://example.com/user1.jpg',
    },
    text: '这是一条评论内容',
    timestamp: '2024-04-29 10:00',
  },
  {
    id: 2,
    user: {
      username: '用户2',
      profile_picture: 'https://example.com/user2.jpg',
    },
    text: '这是另一条评论内容',
    timestamp: '2024-04-29 11:00',
  },
]);
onMounted(async () => {
  try {
    const { data } = await getproductbyid(route.params.id as string);
    product.value = data;

    // 解析 cover_list 字符串，提取图片 URL
    if (data.cover_list) {
      coverListarr.value = data.cover_list.split(',').map(url => url.trim());
    }
    console.log(data);
    try {
      const publishReponse=await getuseradd(data.user_id)
      pubulisher.value=publishReponse.data
      console.log(publishReponse);
      
      
    } catch (error) {
      console.error('获取发布者信息失败', error);
    }
  } catch (error) {
    console.error('获取商品详情失败', error);
  }

  try {
    const myResponse=await getuser();
    me.value=myResponse.data

  } catch (error) {
    console.error('获取本人用户信息失败', error);
  }


  try {
    const prointeraction=await getprointeraction(product.value.id);
    interaction.value=prointeraction.data

  } catch (error) {
    console.error('获取商品被想要/收藏/浏览数失败', error);
  }

  
  
});

const handlebuy=()=>{
  dialogVisible.value=true
}

const handleChange = (value: number | undefined) => {
  console.log(value)
}

const handlewant=async()=>{
  try {
    const { data } = await getinteraction({
      user_id:me.value.id,
      product_id:product.value.id,
      type:3});
    console.log(data,'sidubc')

   
  } catch (error) {
    console.error('想要失败', error);
  }
}
const handleCollect=async()=>{
  try {
    const { data } = await getinteraction({
      user_id:me.value.id,
      product_id:product.value.id,
      type:2});
    console.log(data,'sidubc')

   
  } catch (error) {
    console.error('想要失败', error);
  }
}
</script>

<template>
  <div class="wrapper">
    <div class="left">
      <el-carousel height="150px">
        <el-carousel-item v-for="item in coverListarr" :key="item">
          <img :src="item" alt="" class="responsive-image" />
        </el-carousel-item>
      </el-carousel>
    </div>
    <div class="right"  v-if="product && pubulisher && me">
      <div class="right-header1">
        <span  style="color: red; font-size: 18px;">￥ {{ product.price }} </span>
        <span style="font-size: 14px;">{{ product.category_name }}</span>
        <span>|</span>
        <span style="font-size: 14px;">{{ pubulisher.username }}</span>
        <el-tag type="primary" v-if="product.is_bargain">支持砍价</el-tag>
        <el-tag type="info" v-else>不支持砍价</el-tag>
        
      </div>
      <div class="right-header2">
        {{interaction.want_count}}人想要 · {{interaction.favorite_count}}人收藏 · {{interaction.browse_count}}人浏览
      </div>
      <div style="font-size: 18px; font-weight: 500;">{{ product.name }}</div>
      <el-button-group>
        <el-button type="primary"  class="rounded-button1" @click="handlewant">我想要</el-button>
        <el-button type="info" class="rounded-button2" @click="handlebuy">
          立即购买
        </el-button>
        <el-dialog v-model="dialogVisible" :modal="false">
          <template #header>
            商品下单
          </template>
          <div class="right-header1">
            <span  style="color: red; font-size: 18px;">￥ {{ product.price }} </span>
            <span style="font-size: 14px;">{{ product.category_name }}</span>
            <span>|</span>
            <span style="font-size: 14px;">{{ pubulisher.username }}</span>
            <el-tag type="primary" v-if="product.is_bargain">支持砍价</el-tag>
            <el-tag type="info" v-else>不支持砍价</el-tag>
          </div>
          <div style="font-size: 18px; font-weight: 500; margin-bottom: 10px;">{{ product.name }}</div>
          <div style="margin-bottom: 10px;">下单数量</div>
          <el-input-number v-model="num" :min="1" :max="10" size="small" @change="handleChange" />
          <div style="margin-bottom: 10px;">备注信息</div>
          <el-input
            v-model="textarea"
            style="width: 240px;margin:0 10px;"
            :rows="2"
            type="textarea"
            placeholder="请填写下单备注信息"
            :autosize="{ minRows: 2, maxRows: 4 }"
          />
          <template #footer>
            <div class="dialog-footer">
              <el-button @click="dialogVisible = false">取消下单</el-button>
              <el-button type="primary" @click="dialogVisible = false">
                确定下单
              </el-button>
            </div>
          </template>
        </el-dialog>
        <el-button style="margin-left: 200px; border-radius: 20px;" type="info" @click="handleCollect">收藏</el-button>
      </el-button-group>
      <div class="commet">
        <div>评论</div>
        <el-avatar :size="50" :src="me.profile_picture" />
        <el-input
          v-model="textarea"
          style="width: 240px;margin:0 10px;"
          :rows="2"
          type="textarea"
          placeholder="请友好交流"
          maxlength="300"
          show-word-limit
          :autosize="{ minRows: 2, maxRows: 4 }"
        />
        <el-button>评论</el-button>
        <div class="comment-list">
          评论区待实现
        </div>
      </div>
    </div>
    
  </div>
</template>

<style scoped lang="less">
.wrapper{
  margin-left:100px;
  padding:30px;
  display: flex;
  .left{
    width: 300px;
    height: 100%;
    .demonstration {
      color: var(--el-text-color-secondary);
    }

    .el-carousel__item {
      display: flex;
      justify-content: center;
      align-items: center;

      img {
        width: 100%; /* 设置宽度为 100% */
        height: 100%; /* 设置高度为 100% */
        object-fit: contain
      }
    }

  }
  .right{
    margin-left: 50px;
    flex:1;
    display: flex;
    flex-direction: column;
    gap: 10px; /* 添加间距 */
    .right-header1 {
      display: flex;
      align-items: flex-start;
      gap: 10px; /* 添加间距 */
    }

    span {
      margin-bottom: 5px; /* 为每个 span 添加底部间距 */
    }
    .rounded-button1 {
      border-radius: 20px 0  0 20px; /* 设置较大的 border-radius 值 */
      padding: 10px 20px; /* 调整内边距以适应椭圆形状 */
    }
    .rounded-button2 {
      border-radius: 0 20px  20px 0; /* 设置较大的 border-radius 值 */
      padding: 10px 20px; /* 调整内边距以适应椭圆形状 */
    }
  }
}
</style>