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
        <el-page-header @back="goBack" content="批阅报告"> </el-page-header>
        <div class="projectinfo">
          <span>{{ "学号：" + project.STID }}</span>
          <el-divider direction="vertical"></el-divider>
          <span>{{ "姓名：" + project.name }}</span>
          <span class="cor_now">
            <span>未完成: </span>
            <span class="marginright20">{{ unfinishednum }}</span>
            <span>已批改: </span>
            <span class="colorgreen marginright20" >{{ finishednum }}</span>
            <span>待批改: </span>
            <span class="colorred">{{ correctindex+1 }}</span>
            <span> / </span>
            <span>{{ correcttotal }}</span>
          </span>
        </div>
      </div>
      <div class="content">
        <h4>学生答案：</h4>
        <preview :edithtml="project.report" :files="project.files" :reverse="true"></preview>
        <h4>批语：</h4>
        <el-input
          type="textarea"
          placeholder="请输入内容"
          v-model="project.piyu"
          maxlength="200"
          show-word-limit
          autosize
        >
        </el-input>
      </div>
      <div class="addgrade">
        <div>
          <el-form
            :model="project"
            :rules="FormRules"
            ref="FormRef"
            label-width="55px"
            @submit.native.prevent
          >
            <el-form-item label="得分" prop="grade">
              <el-input v-model.number="project.grade" ref="gradeInput"></el-input>
            </el-form-item>
          </el-form>
        </div>
        <div class="btn-group">
          <el-button-group>
            <el-button type="primary" icon="el-icon-arrow-left" :disabled="correctindex==0" size="mini"
              @click="pre" >上一个</el-button
            >
            <el-button type="primary" size="mini" @click="finish(false)">完成</el-button>
            <el-button type="primary" size="mini" :disabled="correctindex==correcttotal-1"
              @click="next" >下一个<i class="el-icon-arrow-right el-icon--right"></i
            ></el-button>
          </el-button-group>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import Preview from "../common/preview";
import Editarea from "../common/editarea";
import { SEARCHSUBMITLIST , SUBMITGRADE} from "@/network/teacher";
export default {
  name: "",
  components: {
    Preview,
    Editarea,
  },
  data() {
    var checkvalue = (rule, value, callback) => {
      if (value) {
        if (value > 100 || value < 0) {
          callback(new Error("分数范围为0~100"));
        } else {
          callback();
        }
      }
      callback();
    };
    return {
      project: {
        recordID: "1",
        STID: "2017212212127",
        name: "麻富源",
        content: `<p>实验现象：Ⅰ中铁钉生锈，Ⅱ中铁钉不生锈，Ⅲ中铁钉不生锈。</p><p>实验结论：铁生锈的过程实际上是铁与空气中的氧气和水蒸气发生化学反应的过程。</p>`,
        piyu: "",
        grade: "",
      },
      correctindex: 0,
      correcttotal: 0,
      FormRules: {
        grade: [
          { required: true, message: "请输入分数", trigger: "blur" },
          { type: "number", message: "得分必须为数字值", trigger: "blur" },
          { validator: checkvalue, trigger: "blur" },
        ],
      },
      waitcorrectlist:[],
      finishedlist:[],
      correctlist:[],
      finishednum:0,
      unfinishednum:0,
      EXPID:''
    };
  },
  created() {
      this.EXPID = window.sessionStorage.getItem("EXPID");
  },
  mounted() {
      window.addEventListener("keydown", this.keyDown);
      // this.$refs.gradeInput.focus();
      SEARCHSUBMITLIST(this.EXPID, 'all').then((res) => {
        let list=res.data.submitlist;
        this.waitcorrectlist = list.filter(item=>{
          return item.status=='1'
        })
        this.finishedlist=list.filter(item=>{
          return item.status=='2'
        })
        this.unfinishednum=list.filter(item=>{
          return item.status=='0'
        }).length;
        this.finishednum=list.filter(item=>{
          return item.status=='2'
        }).length;
        this.correctindex=this.finishedlist.length;
        if(this.waitcorrectlist.length==0){
          this.correctindex-=1
        }
        this.correctlist.push(...this.finishedlist)
        this.correctlist.push(...this.waitcorrectlist)
        this.correcttotal=this.correctlist.length;

        this.project=JSON.parse(JSON.stringify(this.correctlist[this.correctindex]))

      });
  },
  methods: {
    goBack() {
      this.$router.push({ path: "/home/correctproject" });
    },
    keyDown(e) {
      if (e.keyCode == 13 && this.$refs.gradeInput.focused == true) {
          this.$refs.FormRef.validate(valid=>{
              if(!valid) return;
              
                this.finish(true)
                
                
  
                  
          })
        
      }
    },
    clear(){
       this.$refs.FormRef.resetFields();
    },
    pre(){
              if(this.project.grade==''){
          this.clear();
        }
      if(this.correctindex>0){
        this.correctindex-=1;
        this.project=JSON.parse(JSON.stringify(this.correctlist[this.correctindex]))

      }
    },
    next(){
      if(this.project.grade==''){
          this.clear();
        }
      if(this.correctindex<this.correcttotal-1){
        this.correctindex+=1;
        this.project=JSON.parse(JSON.stringify(this.correctlist[this.correctindex]))
        
      }
    },
    finish(step=false){
       this.$refs.FormRef.validate(valid=>{
              if(!valid) return;
          SUBMITGRADE(this.project).then(res=>{
            let status = res.data.status;
          if (status == "success") {
            this.$message({
              message: "保存成功",
              type: "success",
              duration: 2000,
            });
            this.correctlist[this.correctindex].grade=this.project.grade;
            this.correctlist[this.correctindex].piyu=this.project.piyu;
            if(this.correctlist[this.correctindex].status=='1'){
              this.correctlist[this.correctindex].status=='2';
              this.finishednum+=1
            }
            if(step){
              this.next();
              this.$refs.gradeInput.focus();
            }
          } else {
            this.$message.error("保存失败");
          }
          })
          })
    }
  },
   destroyed() {
    window.removeEventListener("keydown", this.keyDown, false);
  },
};
</script>
<style lang='less' scoped>
.content {
  width: 65%;
  margin: 0 auto;
}
.projectinfo {
  color: #a8b0ce;
  font-size: 12px;
}
.cor_now {
  margin-left: 50px;
  font-size: 18px;
  color: #303133;
}
.colorred {
  color: red;
}
.colorgreen{
  color: green;
}
.marginright20{
  margin-right:20px;
}
.addgrade {
  width: 15%;
  position: fixed;
  top: 200px;
  right: 37px;
  padding: 15px;
  border-radius: 10px;
  // background: #F5F7FA;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}
.btn-group {
  text-align: center;
  margin-top: 20px;
}
</style>