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
        <el-page-header @back="goBack" content="编辑信息"> </el-page-header>
        <div>
          <span class="classtit">发布班级：</span>
          <span>{{project.classno }}</span>
          <el-divider direction="vertical"></el-divider>
          <span v-if="project.issub==0">
            <el-button type="info" @click="saveandnopub">暂时保存</el-button>
            <el-button type="success" @click="saveandpub">发布实验</el-button>
          </span>
          <el-button type="success" v-if="project.issub==1" @click="saveandnopub">保存修改</el-button>
        </div>
      </div>
      <el-container>
        <el-aside width="400px">
          <el-form
            :model="project"
            :rules="editrules"
            ref="ruleForm"
            label-width="85px"
          >
            <el-form-item label="实验标题" prop="title">
              <el-col :span="23">
                <el-input v-model="project.title" placeholder="请输入实验标题"></el-input>
              </el-col>
            </el-form-item>
            <el-form-item label="开始时间" prop="start">
              <el-col :span="23" prop="start">
                <el-form-item>
                  <el-date-picker
                    type="datetime"
                    value-format="yyyy-MM-dd HH:mm:ss"
                    placeholder="选择日期"
                    v-model="project.start"
                    style="width: 100%"
                  ></el-date-picker>
                </el-form-item>
              </el-col>
            </el-form-item>
            <el-form-item label="结束时间" prop="end">
              <el-col :span="23">
                <el-form-item>
                  <el-date-picker
                    type="datetime"
                    value-format="yyyy-MM-dd HH:mm:ss"
                    placeholder="选择日期"
                    v-model="project.end"
                    style="width: 100%"
                  ></el-date-picker>
                </el-form-item>
              </el-col>
            </el-form-item>
          </el-form>
        </el-aside>
        <el-main
          >
          <!-- <el-button @click="sss">dsssss</el-button> -->
          <div class="item">预览</div>
          <preview :edithtml="tempcontent" :files="project.files" ></preview>
          <div class="item">编辑内容</div>
          <editarea :edithtml="project.content" :isshow="true" :files="project.files" @changetxt="updatetxt" @changefilelist="updatefiles"></editarea>
        </el-main>
      </el-container>
    </el-card>
  </div>
</template>

<script>


import Preview from "../common/preview";
import Editarea from "../common/editarea";
import {GETPROJECTINFO,UPDATEPROJECTINFO,UPDATEANDPUB} from "@/network/teacher"
import { formatDate } from "@/common/utils";
export default {
  name: "",
  components: {
    Preview,
    Editarea,
  },
  data() {
    var checktimevalid = (rule, value, cb) => {
      if (value<this.project.start) {
        return cb(new Error("结束时间应大于开始时间"));
      }
      cb();
    };
    return {
      project: {
      
      },
      editrules: {
        title: [{ required: true, message: "请输入标题", trigger: "blur" }],
        start: [
          {
            required: true,
            message: "请输入开始时间",
            trigger: ["blur", "change"],
          },
           
        ],
        end: [
          {
            required: true,
            message: "请输入结束时间",
            trigger: ["blur", "change"],
          },
          { validator: checktimevalid,  trigger: ["blur", "change"]},
        ],
      },
      EXPID:'',
      tempcontent:''
    };
  },
  created() {
    this.EXPID=window.sessionStorage.getItem('EXPID')
    this.getprojectinfo();
  },
  mounted() {
    this.tempcontent=this.project.content;
  },
  methods: {
    goBack() {
      window.sessionStorage.removeItem("EXPID");
      this.$router.push({ path: "/home/projects" });
    },
    getprojectinfo(){
      GETPROJECTINFO(this.EXPID).then(res=>{
        this.project=res.data.project
        console.log(this.project)
        // console.log(res.data)
      })
    },
    sss() {
      this.$refs.ruleForm.validate((valid) => {
        if (!valid) return;
        console.log(this.project.start<this.project.end);
      });
    },
    updatetxt(html){
      this.tempcontent=html
    },
    updatefiles(file){
      this.project.files.unshift(file);
    },
    saveandnopub(){
      this.project.content=this.tempcontent
         this.$refs.ruleForm.validate((valid) => {
        if (!valid) return;
        UPDATEPROJECTINFO(this.project,true).then(res=>{
           let status=res.data.status
          if(status=="success"){
             this.$message({
            message: "保存成功",
            type: "success",
            duration: 2000,
          });
          this.goBack()
          }else{
            this.$message.error("保存失败");
          }
        })
      });
    },
    saveandpub(){
      this.project.content=this.tempcontent

      this.$refs.ruleForm.validate((valid) => {
        if (!valid) return;
        if(this.project.end<=formatDate(new Date(),'YYYY-MM-dd hh:mm:ss')){
          this.$message.error('结束时间应大于当前时间');
          return;
        }
        UPDATEANDPUB(this.project,true).then(res=>{
           let status=res.data.status
          if(status=="success"){
             this.$message({
            message: "发布成功",
            type: "success",
            duration: 2000,
          });
          this.goBack()
          }else{
            this.$message.error("发布失败");
          }
        })
      });
    }
  },
};
</script>
<style lang='less' scoped>
.el-aside {
  background: #fff;
  border-right: 1px solid #ebeef5;
}
.el-main {
  background: #fff;
}
.item {
  font-size: 20px;
  border-bottom: 1px solid #eeeeee;
  color: #606266;
  margin-bottom: 5px;
}

</style>