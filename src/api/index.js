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

//获取所有商品
export const getallproduct=()=>{
  return request.get('/products')
}

//根据用户id获取用户信息，用于在所有商品界面获得发布该商品的用户头像和用户名
export const getuseradd=(userId)=>{
  return request.get(`/users/${userId}/`)
}

//根据商品id获取商品信息，用于商品详情页/商品编辑页
export const getproductbyid=(productId)=>{
  return request.get(`/products/${productId}`)
}

//编辑商品接口
export const editproduct=(productId,data)=>{
  return request.patch(`/products/${productId}/update/`,data)
}

//删除商品接口
export const delproduct=(productId)=>{
  return request.delete(`/products/${productId}/delete/`)
}

//获取分类id,或者是否支持砍价或者某个价格区间的商品的商品
export const getcategorypro=(params)=>{
  const query = new URLSearchParams(params).toString();
  return request.get(`/products/?${query}`)
}

//添加互动行为
export const getinteraction=(data)=>{
  return request.post(`/interactions/`,data)
}
// 获取所有已经想要过的商品
export const getwant=()=>{
  return request.get(`/interactions/want/`)
}

// 获取所有已经收藏过的商品
export const getcollection=()=>{
  return request.get(`/interactions/favorite/`)
}

//取消收藏

export const cancelcollection=(productId)=>{
  return request.post(`/interactions/unfavorite/`,productId)
}

//获取用户是否收藏了某个商品

export const getcollectionboolean=(productId)=>{
  return request.get(`/interactions/is-favorite/?product_id=${productId}`)
}
// 获取单个商品对应的被想要/收藏/浏览数

export const getprointeraction=(productId)=>{
  return request.get(`/interactions/stat/?product_id=${productId}`)
}

//获取用户浏览过的所有商品

export const getfootprint=()=>{
  return request.get(`/interactions/browsed/`)
}

//下单接口
export const order=(data)=>{
  return request.post(`/orders/create/`,data)
}