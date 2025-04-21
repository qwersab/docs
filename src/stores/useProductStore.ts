import { defineStore } from "pinia";
import { getmyproduct } from "@/api";

export const useUserProductStore=defineStore('userProduct',{
  state:()=>({
    products:[] as any[]// 存储用户发布的商品列表
  }),
  actions:{
    async fetchProducts(){
      try{
        const response=await getmyproduct()
        this.products=response.data

      }catch(error){
        console.log('获取商品失败',error);
      }
    }
  }

})