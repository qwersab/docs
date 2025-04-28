import { defineStore } from "pinia";
import { getallproduct } from "@/api";

export const allProductStore=defineStore('allproduct',{
  state:()=>({
    products:[]// 存储所有用户发布的商品列表
  }),
  actions:{
    async fetchProducts(){
      try{
        const response=await getallproduct()
        this.products=response.data

      }catch(error){
        console.log('获取所有商品失败',error);
      }
    }
  }
})