import { defineStore } from "pinia";
import { getallproduct,getcategorypro } from "@/api";

export const allProductStore=defineStore('allproduct',{
  state:()=>({
    products:[],// 存储所有用户发布的商品列表
    filteredProducts: [], // 存储筛选后的商品列表
    isLoading: false, // 加载状态
    filterConditions: {
      categoryId: undefined,
      minPrice: undefined,
      maxPrice: undefined,
      isBargain: undefined,
    },
  }),
  actions:{
    async fetchProducts(){
      this.isLoading = true;
      try{
        const response=await getallproduct()
        this.products=response.data
        this.filteredProducts = response.data; // 初始化筛选列表为全部商品
      }catch(error){
        console.log('获取所有商品失败',error);
      }finally {
        this.isLoading = false;
      }
    },

    async fetchFilteredProducts(){
      const { categoryId, minPrice, maxPrice, isBargain } = this.filterConditions;
      const params = {};
      if (categoryId !== undefined) {
        params['category'] = categoryId;
      }

      if (minPrice !== undefined && maxPrice !== undefined) {
        params['min_price'] = minPrice;
        params['max_price'] = maxPrice;
      }

      if (isBargain !== undefined) {
        params['is_bargain'] = isBargain;
      }


      try {
        const response = await getcategorypro(params);
        this.filteredProducts = response.data;
      } catch (error) {
        console.error('获取筛选商品失败', error);
        this.filteredProducts = []; // 如果失败，清空筛选列表
      }
    },

    updateFilterConditions(newConditions: Partial<typeof this.filterConditions>) {
      this.filterConditions = { ...this.filterConditions, ...newConditions };
      this.fetchFilteredProducts();
    },

  }

})