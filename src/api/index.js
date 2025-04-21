import request from '../utils/request'

// 登录接口
export const login = (data) => {
  return request.post('/login/', data)
}

// 注册接口
export const register = (data) => {
  return request.post('/register/', data)
}

//获取用户信息接口
export const getuser=()=>{
  return request.get('/user/')
}

//修改用户信息接口
export const modifyuser=(data)=>{
  return request.patch('/user/update/',data)
}

//上传头像接口
export const uploadpicture=(file)=>{
  const formData=new FormData()
  formData.append('profile_picture', file);
  return request.post('/user/upload-avatar/',formData,{
    headers: {
      'Content-Type': 'multipart/form-data' // 设置文件上传的Content-Type
    }
  })
}

//修改密码接口
export const modifypwd=(data)=>{
  return request.post('/user/change-password/',data)
}

//上传产品图，多图上传接口
export const uploadimages=(files)=>{
  const formData=new FormData()
  files.forEach((file, index) => {
    formData.append('images[]', file); // 将每个文件添加到 images[] 数组中
  });
  return request.post('/products/upload-image/',formData,{
    headers: {
      'Content-Type': 'multipart/form-data' // 设置文件上传的Content-Type
    }
  })
}

//发布商品接口
export const addproduct=(data)=>{
  return request.post('/products/create/',data)
}

//获取我发布的商品
export const getmyproduct=()=>{
  return request.get('/user/products/')
}