<script setup lang="ts">
import { reactive, ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import type { FormItemProps, FormProps,UploadProps, UploadUserFile,TagProps} from 'element-plus'
import { uploadimages ,addproduct} from '@/api'
import {ElMessage} from 'element-plus'

const labelPosition = ref<FormProps['labelPosition']>('top')
const itemLabelPosition = ref<FormItemProps['labelPosition']>('')
const formLabelAlign = reactive({
  name: '',
  categoryId:1,
  coverList:[],
  detail:'',
  inventory:1,
  isBargain:false,
  oldLevel: 9,
  price: 1,
})
const fileList = ref([])//上传的文件列表
const dialogImageUrl = ref('')//预览图片url
const dialogVisible = ref(false)//控制预览对话框显示

const categoryMap = new Map<string, number>([
  ['书本', 1],
  ['手机', 2],
  ['衣服', 3],
  ['其他', 4],
]);

//删除图片
const handleRemove: UploadProps['onRemove'] = (uploadFile, uploadFiles) => {
  console.log(uploadFile, uploadFiles)
}

//预览图片
const handlePictureCardPreview: UploadProps['onPreview'] = (uploadFile) => {
  dialogImageUrl.value = uploadFile.url!
  dialogVisible.value = true
}


// 自定义上传逻辑
const customUploadRequest = async (options: any) => {
  let files;
  if (options.fileList) {
    files = options.fileList.map((file: any) => file.raw);
  } else if (options.file) {
    files = [options.file];
  } else {
    console.error('未找到文件对象');
    options.onError('未找到文件对象');
    return;
  }

  try {
    const response = await uploadimages(files); // 调用上传接口
    console.log('上传成功', response);
    //图片url在responsr.data.urls里
     console.log(response.data.urls);
    

    // 更新 fileList 中的文件信息
    if (response.data && Array.isArray(response.data.urls)) {
      response.data.urls.forEach((item: any, index: number) => {
        const urlMatch = item.match(/http[s]?:\/\/[^"]+/);
        if(urlMatch){
          const url = urlMatch[0];
          if (fileList.value[index]) {
          fileList.value[index].url = url; 
          console.log(url);
          }
        }else{
          console.error("无法提取有效的 URL", item);
        }
        
      });
    }

    ElMessage.success('图片上传成功');
    options.onSuccess('success');
  } catch (error) {
    console.error('上传失败', error);
    ElMessage.error('图片上传失败');
    options.onError(error);
  }
};


// 上传前的验证
const beforeUpload = (file: File) => {
  const isImage = file.type.startsWith('image/');
  const isLt2M = file.size / 1024 / 1024 < 2;

  if (!isImage) {
    ElMessage.error('上传文件只能是图片格式');
    return false;
  }
  if (!isLt2M) {
    ElMessage.error('上传图片大小不能超过 2MB');
    return false;
  }
  return true;
}


type Item = { type: TagProps['type']; label: string }

const items = ref<Array<Item>>([
  { type: 'primary', label: '书本' },
  { type: 'info', label: '手机' },
  { type: 'info', label: '衣服' },
  { type: 'info', label: '其他' },
])

const submitProduct=async()=>{
  // 确保所有图片已上传完成
  const unfinished = fileList.value.filter(file => file.status !== 'success');
  if (unfinished.length > 0) {
    ElMessage.warning('请等待所有图片上传完成');
    return;
  }
  try {
    const coverList=fileList.value.map((file:any)=>file.url)

    const productData={
      name:formLabelAlign.name,
      category_id:formLabelAlign.categoryId,
      cover_list: coverList,
      detail: formLabelAlign.detail,
      inventory: formLabelAlign.inventory,
      is_bargain: formLabelAlign.isBargain,
      old_level: formLabelAlign.oldLevel,
      price: formLabelAlign.price,
    }
    console.log('提交的数据:', productData); // 打印提交的数据

    const response = await addproduct(productData);
    ElMessage.success('商品发布成功');
    console.log('商品发布成功', response.data);

  }catch (error) {
    ElMessage.error('商品发布失败');
    console.error('商品发布失败', error);
  }

}




</script>

<template>
  <div class="parent">
    <div class="left">
      <el-form
        :label-position="labelPosition"
        label-width="auto"
        :model="formLabelAlign"
        style="max-width: 600px"
      >
        <el-form-item label="商品名" :label-position="itemLabelPosition">
          <el-input v-model="formLabelAlign.name" />
        </el-form-item>
        <el-form-item label="新旧程度" :label-position="itemLabelPosition">
          <el-input-number v-model="formLabelAlign.oldLevel" :step="2" />
        </el-form-item>
        <el-form-item label="价格" :label-position="itemLabelPosition">
          <el-input v-model="formLabelAlign.price" />
        </el-form-item>
        <el-form-item label="是否支持砍价" :label-position="itemLabelPosition">
          <el-switch
            v-model="formLabelAlign.isBargain"
            class="mb-2"
            active-text="支持"
            inactive-text="不支持"
          />
        </el-form-item>
      </el-form>
      <el-button type="primary" @click="submitProduct">发布商品</el-button>
    </div>
    <div class="right">
      <el-form
        :label-position="labelPosition"
        label-width="auto"
        :model="formLabelAlign"
        style="max-width: 600px"
      >
        <el-form-item label="产品图" :label-position="itemLabelPosition">
          <el-upload
            v-model:file-list="fileList"
            action=""
            list-type="picture-card"
            :before-upload="beforeUpload"
            :on-preview="handlePictureCardPreview"
            :on-remove="handleRemove"
            :http-request="customUploadRequest"
            
          >
            <el-icon><Plus /></el-icon>
          </el-upload>

          <el-dialog v-model="dialogVisible">
            <img w-full :src="dialogImageUrl" alt="Preview Image" />
          </el-dialog>
        </el-form-item>
        <el-form-item label="产品类别" :label-position="itemLabelPosition">
          <el-select v-model="formLabelAlign.categoryId" placeholder="请选择分类">
            <el-option
              v-for="item in items"
              :key="item.label"
              :label="item.label"
              :value="categoryMap.get(item.label)"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="库存" :label-position="itemLabelPosition">
          <el-input-number v-model="formLabelAlign.inventory" :step="2" />
        </el-form-item>
        <el-form-item label="商品描述" :label-position="itemLabelPosition">
          <el-input type="textarea" v-model="formLabelAlign.detail" />
        </el-form-item>
        

      </el-form>
    </div>

  </div>

</template>

<style scoped lang="less">
.parent{
  margin: 20px;
  display: flex;
  .left{
    width: 400px;
    height: 100%;
  }
  .right{
    flex: 1;
    margin-left: 50px;
    height: 100%;
  }
}
</style>