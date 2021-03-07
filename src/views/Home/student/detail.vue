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
        <el-page-header @back="goBack" :content="TEproject.title">
        </el-page-header>
        <div class="projectinfo">
          <span>{{ "作答时间：" + TEproject.start + "至" + TEproject.end }}</span>
          <el-divider direction="vertical"></el-divider>
          <span class="grade" v-if="status==3"
            ><i>{{ STproject.grade }}</i
            >分</span
          >
        </div>
      </div>
      <div class="content">
      
        <preview :edithtml="TEproject.content" :files="TEproject.files"></preview>

        <el-divider></el-divider>
        <h4>我的答案：</h4>
        <editarea :isshow="status==1 || status==2" :files="STproject.files" :edithtml="STproject.report" @changetxt="updatetxt" @changefilelist="updatefiles"></editarea>

        <div class="submit" v-if="status==1 || status==2">
          <el-button size="small" v-if="status==1" @click="temporarysave">暂时保存</el-button>
          <el-button size="small" type="success" @click="submitoredit">{{
            status==1 ? "提交报告" : "修改报告"
          }}</el-button>
        </div>
        
        <div v-if="status==3||status==4">
          <preview :edithtml="STproject.report" :reverse="true" :files="STproject.files"></preview>
          <div >
          <h4 style="color:green">正确答案：</h4>
          <preview :edithtml="TEproject.anscontent" :files="TEproject.ansfiles" :reverse="true"></preview>
          </div>
          <div v-if="STproject.piyu!=''">
            <h4>老师批语：</h4>
            <div v-html="STproject.piyu"></div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import E from "wangeditor";
import Preview from "../common/preview";
import Editarea from "../common/editarea";
import {GETDETAIL,SAVEANDSUB} from '@/network/student';
import { formatDate } from "@/common/utils";

export default {
  name: "",
  components: {
    Preview,
    Editarea,
  },
  data() {
    return {
     TEproject:{},
     STproject:{},
      EXPID:'',
      recordID:'',
      status:'',
      tempreport:''
    };
  },
  created() {
    this.EXPID=window.sessionStorage.getItem('EXPID')
    this.recordID=window.sessionStorage.getItem('recordID')
    this.status=window.sessionStorage.getItem('status')
  },
  mounted() {
    this.getdetail()
  },
  methods: {
    goBack() {
      window.sessionStorage.removeItem("EXPID");
      window.sessionStorage.removeItem("recordID");
      window.sessionStorage.removeItem("status");
      this.$router.push({ path: "/home/projects" });
    },
    getdetail(){
GETDETAIL(this.EXPID,this.recordID).then(res=>{
    // console.log(res.data.TEproject)
    // console.log(res.data.STproject.piyu)
    this.TEproject=res.data.TEproject
    this.STproject=res.data.STproject
    this.STproject.piyu=this.STproject.piyu.replace(/\n/g,"<br>")
})
    },
        updatetxt(html){
      this.tempreport=html;
    },
    updatefiles(file){
      this.STproject.files.unshift(file);
    },
  temporarysave(){
    this.STproject.report=this.tempreport;
    this.STproject.subtime=formatDate(new Date(),'YYYY-MM-dd hh:mm:ss');
    SAVEANDSUB(this.STproject,false,true).then(res=>{
      let status=res.data.status
          if(status=="success"){
             this.$message({
            message: "保存成功",
            type: "success",
            duration: 2000,
          });
          }else{
            this.$message.error("保存失败");
          }
    })
  },
  submitoredit(){
    this.STproject.report=this.tempreport;
    this.STproject.subtime=formatDate(new Date(),'YYYY-MM-dd hh:mm:ss');
    if(formatDate(new Date(),'YYYY-MM-dd hh:mm:ss')>=this.TEproject.end){
      this.$message.error('已超过截止时间，无法提交');
      return;
    }
  SAVEANDSUB(this.STproject,true,true).then(res=>{
      let status=res.data.status
          if(status=="success"){
             this.$message({
            message: "提交成功",
            type: "success",
            duration: 2000,
          });
          this.status=2;
          }else{
            this.$message.error("提交失败");
          }
    })
  }
  },
};
</script>
<style lang='less' scoped>
.projectinfo {
  color: #a8b0ce;
  font-size: 12px;
}
.grade {
  color: #f7704e;
  i {
    font-size: 24px;
    font-family: din;
    font-style: normal;
  }
}
.content {
  width: 65%;
  margin: 0 auto;
}


.submit {
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-around;
}
</style>