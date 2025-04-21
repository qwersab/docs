<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { login, register } from '../../api/index.js'; // 引入 API 函数
import { ElMessage ,type FormInstance,type FormRules} from 'element-plus'; // 引入 ElMessage

const route = useRoute();
const router = useRouter();
const formType = ref<'login'|'register'>('login');

//首先进行类型定义
interface UserInfo{
  name:string,
  password:string
}

//继承UserInfo
interface RegisterInfo extends UserInfo{
  email:string
}

interface ApiResponse{
  data:{
      token:string,
    }
    status   
}

//定义表单数据
const userInfo=ref<UserInfo>({
  name:'',
  password:''
})

const registerInfo=ref<RegisterInfo>({
  email: '',
  name: '',
  password: ''

})


// 根据路由参数初始化表单类型
onMounted(() => {
  updateFormType();
});

// 监听路由变化
watch(() => route.path, (newPath) => {
  updateFormType();
});

// 更新表单类型的函数
function updateFormType() {
  if (route.path === '/register') {
    formType.value = 'register';
  } else {
    formType.value = 'login';
  }
  console.log('当前路径:', route.path, '表单类型:', formType.value);
}

// const userInfo=ref({
//   name:'',
//   password:''
// })

// const registerInfo = ref({
//   name: '',
//   password: '',
//   email: ''
// });

const rules:Record<'login'|'register',FormRules>={
  login: {
    name: [
      { required: true, message: '请输入用户名', trigger: 'blur' },
      { min: 3, max: 10, message: '用户名长度在 3 到 10 个字符之间', trigger: 'blur' }
    ],
    password: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 6, max: 18, message: '密码长度在 6 到 18 个字符之间', trigger: 'blur' }
    ]
  },
  register: {
    name: [
      { required: true, message: '请输入用户名', trigger: 'blur' },
      { min: 3, max: 10, message: '用户名长度在 3 到 10 个字符之间', trigger: 'blur' }
    ],
    password: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 6, max: 18, message: '密码长度在 6 到 18 个字符之间', trigger: 'blur' }
    ],
    email: [
      { required: true, message: '请输入邮箱', trigger: 'blur' },
      { type: 'email', message: '请输入有效的邮箱地址', trigger: ['blur', 'change'] }
    ]
  }

}

// 表单引用
//const ruleFormRef = ref(null);

const ruleFormRef = ref<FormInstance>()



// 动态绑定的表单数据,明确返回数据类型
const formData = computed<RegisterInfo|UserInfo>({
  get: () => {
    return formType.value === 'login' ? userInfo.value : registerInfo.value;
  },
  set: (value:RegisterInfo|UserInfo) => {
    if (formType.value === 'login') {
      userInfo.value = value as UserInfo;
    } else {
      registerInfo.value = value as RegisterInfo;
    }
  }
});

// 表单提交逻辑
// const handleSubmit = async () => {
//   ruleFormRef.value.validate(async (valid) => {
//     if (valid) {
//       try {
//         if (formType.value === 'login') {
//           // 调用登录接口
//           const res = await login({
//             username: userInfo.value.name,
//             password: userInfo.value.password
//           });
//           console.log('Login response:', res);
//           if (res.data && res.data.token) { // 假设成功响应包含 token
//             localStorage.setItem('tr_token', res.data.token); // 存储 token
//             ElMessage.success('登录成功！');
//             router.push('/'); // 跳转到主页或其他页面
//           } else {
//             ElMessage.error(res.data.message || '登录失败');
//           }
//         } else {
//           // 调用注册接口
//           const res = await register({
//             username: registerInfo.value.name,
//             email: registerInfo.value.email,
//             password: registerInfo.value.password
//           });
//           console.log('Register response:', res);
//           if (res.data && res.data.code === 0) { // 假设注册成功 code 为 0
//             ElMessage.success('注册成功！请登录。');
//             toggleForm(); // 切换到登录表单
//           } else {
//             ElMessage.error(res.data.message || '注册失败');
//           }
//         }
//       } catch (error) {
//         console.error('API call failed:', error);
//         ElMessage.error('请求失败，请检查网络或联系管理员。');
//       }
//     } else {
//       ElMessage.warning('表单验证失败！');
//       return false;
//     }
//   });
// };

const handleSubmit=async():Promise<void>=>{
  if(!ruleFormRef.value) return
  try{
    const valid=ruleFormRef.value.validate()
    if(!valid){
      ElMessage.warning('表单验证失败！');
      return
    }

    let res:ApiResponse
    if(formType.value==='login'){
      res=await login({
        username:userInfo.value.name,
        password:userInfo.value.password
      })
      if(res.data.token&&res.status===200){
        localStorage.setItem('tr_token',res.data.token)
        ElMessage.success('登陆成功')
        router.push('/')
      }else{
        ElMessage.error(res.status || '登录失败');
      }

    }else{
      res=await register({
        username: registerInfo.value.name,
        email: registerInfo.value.email,
        password: registerInfo.value.password
      })
      if(res.data&&res.status===201){
        ElMessage.success('注册成功')
        //切换表单
        toggleForm()
      }else{
        ElMessage.error(res.status || '注册失败');
      }
    }


  }catch(error){
    console.error('API call failed:', error);
    ElMessage.error('请求失败，请检查网络或联系管理员。');

  }
  

}

// 切换表单类型
const toggleForm = () => {
  if (formType.value === 'login') {
    router.push('/register');
  } else {
    router.push('/login');
  }
};


</script>

<template>
  <div class="bigbox">
    <div class="left">
      <img src="../../images/logo.jpg" alt="">
    </div>
    <div class="right">
      <div>校园二手交易平台</div>
      <el-form
        ref="ruleFormRef"
        style="max-width: 600px"
        :model="formData"
        :rules="rules[formType]"
        label-width="auto"
        class="demo-ruleForm"
        status-icon
      >
        <el-form-item label="账号" prop="name">
          <el-input v-model="formData.name" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="formData.password" type="password" />
        </el-form-item>
        <el-form-item v-if="formType === 'register'" label="邮箱" prop="email">
          <el-input v-model="(formData as RegisterInfo).email" type="email" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">{{ formType === 'login' ? '登录' : '注册' }}</el-button>
        </el-form-item>
      </el-form>
      <div>
        <span v-if="formType === 'login'">没有账号？</span>
        <span v-else>已有账号？</span>
        <a href="javascript:void(0);" @click="toggleForm">{{ formType === 'login' ? '点击注册' : '点击登录' }}</a>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.bigbox{
  margin: auto;
  display: flex;
  justify-content: space-around;
  width: 600px;
  height: 300px;
  background-color: #b1def4;
  border-radius:100px 10px 10px 10px;
  .left{
    margin-top: 50px;

    img{
      width: 200px;
      height: 200px;
      clip-path: circle(40%);
    }

  }
  
  .right{
    margin-top: 20px;
    width: 250px;
    height: 260px;
    padding: 0 20px;
    background-color: white;
    .el-button {
      width: 100%;
    }
    
  }
}

</style>