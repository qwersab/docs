<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { getproductbyid ,getuseradd,getuser,getinteraction,getprointeraction, getcollectionboolean, cancelcollection, order, getComments, comments as postComment } from '@/api';
import { UserFilled } from '@element-plus/icons-vue';
import { useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import CommentItem from '@/components/CommentItem.vue';
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
const comments = ref([]);
const commentContent = ref('');
const loadingComments = ref(false);
const isCollected = ref(false);
const orderLoading = ref(false);
const replyToId = ref(null); // 当前要回复的评论ID
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
    // 只记录浏览，不触发收藏
    const { data } = await getinteraction({
      user_id:me.value.id,
      product_id:product.value.id,
      type:1  // 1表示浏览
    });
  } catch (error) {
    console.error('浏览失败', error);
  }

  try {
    // 获取商品的交互数据（浏览、收藏、想要数量）
    const prointeraction=await getprointeraction(product.value.id);
    interaction.value=prointeraction.data
  } catch (error) {
    console.error('获取商品被想要/收藏/浏览数失败', error);
  }

  // 判断是否已收藏
  try {
    const res = await getcollectionboolean(product.value.id);
    isCollected.value = !!res.data.is_favorite;
  } catch (error) {
    isCollected.value = false;
  }

  await fetchComments();
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

   
  } catch (error) {
    console.error('想要失败', error);
  }
}
const handleCollect = async () => {
  if (!isCollected.value) {
    // 收藏
    try {
      await getinteraction({
        user_id: me.value.id,
        product_id: product.value.id,
        type: 2
      });
      isCollected.value = true;
      interaction.value.favorite_count++;
    } catch (error) {
      // 错误处理
    }
  } else {
    // 取消收藏
    try {
      await cancelcollection({'product_id':product.value.id});
      isCollected.value = false;
      interaction.value.favorite_count--;
    } catch (error) {
      // 错误处理
    }
  }
};

const submitOrder = async () => {
  if (!product.value) return;
  orderLoading.value = true;
  try {
    const res = await order({
      detail: textarea.value ? `买家留言：${textarea.value}` : '',
      product: product.value.id,
      buy_price: (product.value.price * num.value).toFixed(2),
      trade_status: 0
    });
    orderLoading.value = false;
    dialogVisible.value = false;
    ElMessage.success('下单成功，订单号：' + res.data.code);
  } catch (error) {
    orderLoading.value = false;
    ElMessage.error('下单失败，请检查信息');
  }
};

// 递归补充头像字段
const addProfilePicture = (commentsArr) => {
  commentsArr.forEach(comment => {
    // 假设只有自己有头像，其他人用默认
    comment.profile_picture = comment.user_id === me.value.id ? me.value.profile_picture : '';
    if (comment.replies && comment.replies.length > 0) {
      addProfilePicture(comment.replies);
    }
  });
};

const fetchComments = async () => {
  if (!product.value) return;
  loadingComments.value = true;
  try {
    const { data } = await getComments(product.value.id);
    
    // 检查返回的数据结构
    console.log('评论数据:', data);
    
    // 如果后端已经返回了树形结构（带有replies字段），直接使用
    if (data.length > 0 && data[0].replies !== undefined) {
      comments.value = data;
    } else {
      // 如果后端返回的是扁平结构，需要在前端构建树形结构
      // 这里假设每条评论都有 id 和可能的 parent_id 字段
      const commentMap = {};
      const rootComments = [];
      
      // 第一遍遍历，建立映射
      data.forEach(comment => {
        // 确保每个评论都有一个空的replies数组
        comment.replies = [];
        commentMap[comment.id] = comment;
      });
      
      // 第二遍遍历，构建树形结构
      data.forEach(comment => {
        // 检查可能的父评论ID字段名
        const parentId = comment.parent_id || comment.parent || null;
        
        if (parentId) {
          // 这是一个回复，将其添加到父评论的replies中
          const parentComment = commentMap[parentId];
          if (parentComment) {
            parentComment.replies.push(comment);
          } else {
            // 父评论不存在，作为根评论处理
            rootComments.push(comment);
          }
        } else {
          // 这是一个根评论
          rootComments.push(comment);
        }
      });
      
      comments.value = rootComments;
    }
    // 补充头像字段
    addProfilePicture(comments.value);
  } catch (e) {
    ElMessage.error('获取评论失败');
    console.error('获取评论失败:', e);
  }
  loadingComments.value = false;
};

const submitComment = async () => {
  if (!commentContent.value.trim()) {
    ElMessage.warning('评论内容不能为空');
    return;
  }
  try {
    await postComment({
      product_id: product.value.id,
      content: commentContent.value,
      parent_id: null
    });
    ElMessage.success('评论成功');
    commentContent.value = '';
    fetchComments();
  } catch (e) {
    ElMessage.error('评论失败');
  }
};

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
};

// 显示回复表单
const showReplyForm = (commentId) => {
  replyToId.value = commentId;
};

// 取消回复
const cancelReply = () => {
  replyToId.value = null;
};

// 提交回复（适配递归组件，content为参数）
const submitReply = async (parentId, content) => {
  if (!content || !content.trim()) {
    ElMessage.warning('回复内容不能为空');
    return;
  }
  try {
    await postComment({
      product_id: product.value.id,
      content: content,
      parent_id: parentId // 设置父评论ID
    });
    ElMessage.success('回复成功');
    replyToId.value = null;
    fetchComments(); // 重新获取评论列表
  } catch (e) {
    ElMessage.error('回复失败');
  }
};
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
              <el-button type="primary" :loading="orderLoading" @click="submitOrder">
                确定下单
              </el-button>
            </div>
          </template>
        </el-dialog>
        <el-button
          style="margin-left: 200px; border-radius: 20px;"
          :type="isCollected ? 'primary' : 'info'"
          @click="handleCollect"
        >
          {{ isCollected ? '取消收藏' : '收藏' }}
        </el-button>
      </el-button-group>
      <div class="commet">
        <div>评论</div>
        <el-avatar :size="50" :src="me.profile_picture" />
        <el-input
          v-model="commentContent"
          style="width: 240px;margin:0 10px;"
          :rows="2"
          type="textarea"
          placeholder="请友好交流"
          maxlength="300"
          show-word-limit
          :autosize="{ minRows: 2, maxRows: 4 }"
        />
        <el-button @click="submitComment">评论</el-button>
        <div class="comment-list">
          <CommentItem
            v-for="comment in comments"
            :key="comment.id"
            :comment="comment"
            :parentUsername="''"
            :replyToId="replyToId"
            :showReplyForm="showReplyForm"
            :cancelReply="cancelReply"
            :submitReply="submitReply"
            :formatDate="formatDate"
            :me="me"
          />
          <div v-if="comments.length === 0" class="no-comments">
            暂无评论
          </div>
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
  
  .comment-list {
    margin-top: 20px;
    width: 100%;
    
    .comment-item {
      padding: 15px 0;
      border-bottom: 1px solid #f0f0f0;
      
      .comment-header {
        display: flex;
        align-items: center;
        margin-bottom: 8px;
        
        .comment-info {
          margin-left: 10px;
          
          .comment-username {
            font-weight: 500;
            font-size: 14px;
          }
          
          .comment-time {
            font-size: 12px;
            color: #999;
            margin-top: 2px;
          }
        }
      }
      
      .comment-content {
        margin-left: 50px;
        font-size: 14px;
        line-height: 1.5;
        color: #333;
      }
      
      .comment-actions {
        margin-left: 50px;
        margin-top: 5px;
      }
      
      .reply-form {
        margin-left: 50px;
        margin-top: 10px;
        margin-bottom: 15px;
        
        .reply-buttons {
          margin-top: 10px;
          display: flex;
          justify-content: flex-end;
        }
      }
      
      .comment-replies {
        margin-left: 50px;
        margin-top: 10px;
        
        .reply-item {
          padding: 10px;
          background-color: #f9f9f9;
          border-radius: 4px;
          margin-bottom: 8px;
          
          .comment-content {
            margin-left: 40px;
          }
        }
      }
    }
    
    .no-comments {
      text-align: center;
      color: #999;
      padding: 20px 0;
    }
  }
}
</style>