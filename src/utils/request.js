import axios from "axios";
import { ElMessage } from "element-plus";

const instance = axios.create({
  baseURL:'http://127.0.0.1:8000/api',
  timeout: 10000,

}
 
);

// 添加请求拦截器
instance.interceptors.request.use(function (config) {
  // 在发送请求之前做些什么
  const token=localStorage.getItem('tr_token')
  const whiteUrl=['/login','/register']
  if(token&&!whiteUrl.includes(config.url)){
    config.headers['Authorization']=`Token ${token}`

  }
  return config;
}, function (error) {
  // 对请求错误做些什么
  return Promise.reject(error);
});

// 添加响应拦截器
instance.interceptors.response.use(function (response) {
  if(response.data.code===-1){
    ElMessage.warning(response.data.message)

  }
  // 2xx 范围内的状态码都会触发该函数。
  // 对响应数据做点什么
  return response;
}, function (error) {
  // 超出 2xx 范围的状态码都会触发该函数。
  // 对响应错误做点什么
  return Promise.reject(error);
});

export default instance