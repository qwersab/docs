import { createRouter, createWebHashHistory } from 'vue-router'
import Layout from '../views/Main.vue'
import Login from '../views/login/index.vue'
import AllProduct from '../views/producttotal/index.vue'
import MyProduct from '../views/myproduct/index.vue'
import Collection from '../views/collection/index.vue'
import FootPrints from '../views/footprints/index.vue'
import Order from '../views/order/index.vue'
import Notice from '../views/notice/index.vue'
import SubmitProduct from '../views/submitProduct/index.vue'
import Mine  from '../views/mine/index.vue'

function isLoggedIn() {
  // return !!localStorage.getItem('token'); // 假设登录状态存储在 localStorage 中
  return true
}

const routes=[
  {
    path:'/',
    component:Layout,
    name:'main',
    redirect:'/allproduct',
    children:[
      {
        path:'/allproduct',
        component:AllProduct,
        meta:{title:'所有商品',requireAuth:false}
      },
      {
        path:'/myproduct',
        component:MyProduct,
        meta:{title:'我的商品',requireAuth:true}
      },
      {
        path:'/collection',
        component:Collection,
        meta:{title:'我的收藏',requireAuth:true}
      },
      {
        path:'/footprints',
        component:FootPrints,
        meta:{title:'足迹',requireAuth:true}
      },
      {
        path:'/order',
        component:Order,
        meta:{title:'订单',requireAuth:true}
      },
      {
        path:'/notice',
        component:Notice,
        meta:{title:'通知',requireAuth:true}
      },
      {
        path:'/submitproduct',
        component:SubmitProduct,
        meta:{title:'发布商品',requireAuth:true}
      },
      {
        path:'/mine',
        component:Mine,
        meta:{title:'个人中心',requireAuth:true}
      },
      {
        path: '/submitproduct/:id',
        name: 'EditProduct',
        component: () => import('@/views/submitProduct/index.vue')
      }
    ]
  },
  {
    path:'/login',
    component:Login
  },
  {
    path:'/register',
    component:Login
  }
]

const router=createRouter({
  routes,
  history:createWebHashHistory()
})

router.beforeEach((to, from, next)=>{
  if (to.meta.requireAuth && !isLoggedIn()) {
    next('/login'); // 跳转到登录页
  } else {
    next(); // 放行
  }

})

export default router

