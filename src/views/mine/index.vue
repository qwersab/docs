<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import { getuser ,modifyuser,uploadpicture,modifypwd} from '@/api';

interface Form{
  name:string,
  email:string,
  avatar:string
}
const form=ref<Form>({
  name:'',
  email:'',
  avatar:''
})


const currentFormType=ref<string>('profile')
const forms=ref({
  profile:{
    username:'',
    email:'',
    profile_picture:''
  },
  password:{
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  }

})
//强制更新
const uploadKey=ref(0)

const imageUrl = ref('');

const getUserInfo=async():Promise<void>=>{
    const {data}=await getuser()
    forms.value.profile.profile_picture=data.profile_picture
    forms.value.profile.username=data.username
    forms.value.profile.email=data.email
    // 同时设置 imageUrl
    imageUrl.value = data.profile_picture
}


//切换表单逻辑
const switchForm=(formType:string)=>{
  currentFormType.value=formType
}


// 头像上传成功后的回调
const handleAvatarSuccess = (response:any) => {
  const avatarUrl = response.profile_picture;
  // 直接使用返回的URL
  imageUrl.value = avatarUrl;
  forms.value.profile.profile_picture = avatarUrl;
  uploadKey.value += 1;
  ElMessage.success('头像上传成功');
};

const handleAvatarError = (error: any) => {
  ElMessage.error('头像上传失败，请稍后再试');
  console.error('上传失败:', error);
};

// 上传前的回调
const beforeAvatarUpload = async(file:File) => {
  const isJPG = file.type === 'image/jpeg';
  const isPNG = file.type === 'image/png';
  const isLt2M = file.size / 1024 / 1024 < 2;

  if (!isJPG && !isPNG) {
    ElMessage.error('上传头像图片只能是 JPG 或 PNG 格式');
    return false;
  }
  if (!isLt2M) {
    ElMessage.error('上传头像图片大小不能超过 2MB');
    return false;
  }

  try{
    const response=await uploadpicture(file)
    handleAvatarSuccess(response)
  }catch(error){
    handleAvatarError(error)
  }
  return false;
};

// 提交表单
const submitProfileForm = async () => {
  try {
    console.log('提交的个人资料表单数据:', forms.value.profile);
    const response=await modifyuser(forms.value.profile);
    ElMessage.success('用户信息更新成功');
    console.log(response,'更新后');
    
  } catch (error) {
    ElMessage.error('用户信息更新失败，请稍后再试',error);
  }
};

const submitPwdForm=async()=>{
  try{
    const response11=await modifypwd(forms.value.password)
    ElMessage.success('修改密码成功')
    console.log(response11,'修改密码后');
    

  }catch(error){
    ElMessage.error('修改密码失败',error)

  }
}

getUserInfo()

</script>

<template>
  <h2 style="font-weight: 400;">个人中心</h2>
  <el-button type="info" @click="switchForm('profile')">修改资料</el-button>
  <el-button type="info" @click="switchForm('password')">修改密码</el-button>
  <el-button type="info">退出登录</el-button>
  <div v-if="currentFormType==='profile'">
    <el-form :model="forms.profile" label-width="auto" style="max-width: 600px">
      <el-form-item label="头像">
        <el-upload
          class="avatar-uploader"
          action=""
          :show-file-list="false"
          :on-success="handleAvatarSuccess"
          :before-upload="beforeAvatarUpload"
          :key="uploadKey"
        >
          <el-avatar v-if="imageUrl" :src="imageUrl" class="avatar" :fit="'cover'" />
          <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
        </el-upload>
      </el-form-item>
      <el-form-item label="昵称">
        <el-input v-model="forms.profile.username" />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="forms.profile.email" />
      </el-form-item>
    </el-form>
    <el-button @click="submitProfileForm">立即修改</el-button>
  </div>

  <div v-if="currentFormType==='password'">
    <el-form :model="forms.password" label-width="auto" style="max-width: 600px">
      <el-form-item label="原密码" >
        <el-input v-model="forms.password.oldPassword" type="password"/>
      </el-form-item>
      <el-form-item label="新密码">
        <el-input v-model="forms.password.newPassword" type="password"/>
      </el-form-item>
      <el-form-item label="确认密码">
        <el-input v-model="forms.password.confirmPassword" type="password"/>
      </el-form-item>
      
    </el-form>
    <el-button @click="submitPwdForm">立即修改</el-button>
    
  </div>
 

  
</template>

<style scoped>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>