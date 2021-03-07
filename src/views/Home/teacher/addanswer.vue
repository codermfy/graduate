<!--  -->
<template>
<div id="" class="editor">
    <el-card>
        <div
        slot="header"
        class="clearfix"
        style="
          display: flex;
          align-items: center;
          justify-content: space-between;
        "
      >
        <el-page-header @back="goBack" content="添加答案"> </el-page-header>
         <el-button type="success" @click="subans">提交</el-button>
      </div>
     <div class="content">
         <preview :edithtml="project.content" :files="project.files"></preview>
         <el-divider></el-divider>
        <h4 style="color:green">正确答案：</h4>
        <editarea :isshow="true"  :edithtml="project.anscontent" :files="project.ansfiles" @changetxt="updatetxt" @changefilelist="updatefiles"></editarea>
     </div>
    </el-card>
</div>
</template>

<script>
import Preview from "../common/preview";
import Editarea from "../common/editarea";
import { GETPROJECTINFO, UPDATEPROJECTINFO} from "@/network/teacher";
export default {
    name:"",
    components: {
    Preview,
    Editarea,
  },
    data() {
        return {
          project:{},
          EXPID:'',
          tempcontent:''
        }
    },
    created() {
       this.EXPID = window.sessionStorage.getItem("EXPID");
    },
    mounted() {
      GETPROJECTINFO(this.EXPID)
      .then((res) => {
        this.project = res.data.project;

      })
      
    },
    methods:{
        goBack() {
      this.$router.push({ path: "/home/correctproject" });
    },
    updatefiles(file){
      this.project.ansfiles.unshift(file);
    },
    subans(){
      this.project.anscontent=this.tempcontent
      UPDATEPROJECTINFO(this.project,true).then(res=>{
        let status=res.data.status
          if(status=="success"){
             this.$message({
            message: "保存答案成功",
            type: "success",
            duration: 2000,
          });
          this.goBack()
          }else{
            this.$message.error("保存失败");
          }
      })
    },
    updatetxt(html){
      this.tempcontent=html;
    }
    }
}
</script>
<style lang='less' scoped>
.content {
  width: 65%;
  margin: 0 auto;
}
</style>