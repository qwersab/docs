<script setup lang="ts">
import { ref, watch } from 'vue';
import { UserFilled } from '@element-plus/icons-vue';

const props = defineProps<{
  comment: any,
  parentUsername?: string,
  replyToId: number | null,
  showReplyForm: (id: number) => void,
  cancelReply: () => void,
  submitReply: (parentId: number, content: string, parentUsername?: string) => void,
  formatDate: (date: string) => string,
  me?: any
}>();

// 本地的回复内容
const localReplyContent = ref('');
// 如果当前显示的回复表单不是自己，清空内容
watch(() => props.replyToId, (newVal) => {
  if (newVal !== props.comment.id) {
    localReplyContent.value = '';
  }
});
</script>

<template>
  <div class="comment-item">
    <div class="comment-header">
      <el-avatar
        :size="40"
        v-if="comment.profile_picture"
        :src="comment.profile_picture"
      />
      <el-avatar
        :size="40"
        v-else
        :icon="UserFilled"
      />
      <div class="comment-info">
        <div class="comment-username">{{ comment.username }}</div>
        <div class="comment-time">{{ formatDate(comment.create_time) }}</div>
      </div>
    </div>
    <div class="comment-content">
      <span v-if="parentUsername && comment.username !== parentUsername">
        回复 {{ parentUsername }}：
      </span>
      {{ comment.content }}
    </div>
    <div class="comment-actions">
      <el-button type="text" size="small" @click="showReplyForm(comment.id)">回复</el-button>
    </div>
    <!-- 回复表单 -->
    <div v-if="replyToId === comment.id" class="reply-form">
      <el-input
        v-model="localReplyContent"
        type="textarea"
        :rows="2"
        placeholder="请输入回复内容"
        maxlength="300"
        show-word-limit
      />
      <div class="reply-buttons">
        <el-button size="small" @click="cancelReply">取消</el-button>
        <el-button type="primary" size="small" @click="submitReply(comment.id, localReplyContent, comment.username)">提交回复</el-button>
      </div>
    </div>
    <!-- 递归渲染子评论 -->
    <div v-if="comment.replies && comment.replies.length > 0" class="comment-replies">
      <CommentItem
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
        :parentUsername="comment.username"
        :replyToId="replyToId"
        :showReplyForm="showReplyForm"
        :cancelReply="cancelReply"
        :submitReply="submitReply"
        :formatDate="formatDate"
        :me="me"
      />
    </div>
  </div>
</template>

<style scoped>
.comment-item {
  padding: 15px 0;
  border-bottom: 1px solid #f0f0f0;
}
.comment-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}
.comment-info {
  margin-left: 10px;
}
.comment-username {
  font-weight: 500;
  font-size: 14px;
}
.comment-time {
  font-size: 12px;
  color: #999;
  margin-top: 2px;
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
}
.reply-buttons {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
}
.comment-replies {
  margin-left: 50px;
  margin-top: 10px;
}
</style>
