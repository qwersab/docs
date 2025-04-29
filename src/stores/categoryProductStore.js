import { defineStore } from "pinia";
import { getcategorypro } from "@/api";

export const allProductStore=defineStore('fenleiproduct',{
  state:()=>({
    products:[]// 存储分类商品列表
  }),
  actions:{
    async fetchProducts(){
      try{
        const response=await getcategorypro()
        this.products=response.data

      }catch(error){
        console.log('获取分类商品失败',error);
      }
    }
  }
})