<!--  -->
<template>
  <div id="" class="exlist">
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
        <el-page-header @back="goBack" content="批阅信息"> </el-page-header>
        <div>
          <span class="classtit">班级：</span>
          <span>{{ project.classno }}</span>
          <el-divider direction="vertical"></el-divider>
          <span v-if="true">
            <el-button type="success" @click="addans">添加正确答案</el-button>
            <el-button type="primary" @click="correctall">开始批阅</el-button>
          </span>
        </div>
      </div>
      <div class="projecttable">
        <div class="radio">
          <span style="color: #606266">筛选：</span>
          <el-radio-group v-model="querytype">
            <el-radio label="all">全部</el-radio>
            <el-radio label="finished">已完成</el-radio>
            <el-radio label="waitcorrect">待批阅</el-radio>
            <el-radio label="unfinished">未完成</el-radio>
          </el-radio-group>
        </div>
        <el-table :data="projectrecord" border>
          <el-table-column type="index" align="center"></el-table-column>
          <el-table-column prop="STID" label="学号"> </el-table-column>
          <el-table-column prop="name" label="姓名"></el-table-column>
          <el-table-column label="状态" width="70px">
            <template v-slot="scope">
              <p v-if="scope.row.status == '0'" style="color: red">未完成</p>
              <p v-else-if="scope.row.status == '1'">待批阅</p>
              <p v-else-if="scope.row.status == '2'" style="color: green">
                已完成
              </p>
            </template>
          </el-table-column>
          <el-table-column
            prop="subtime"
            label="提交时间"
            sortable
          ></el-table-column>
          <el-table-column prop="grade" label="成绩" sortable width="80px">
          </el-table-column>

          <el-table-column label="操作">
            <template v-slot="scope">
              <el-button
                type="success"
                plain
                size="mini"
                v-if="scope.row.status == '1'"
                @click="piyue(scope.row)"
                >批阅</el-button
              >
              <el-button
                type="primary"
                plain
                size="mini"
                v-if="scope.row.status == '2'"
                @click="edit(scope.row)"
                >修改信息</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
    <el-dialog
  :title="title"
  :visible.sync="dialogVisible"
  width="70%"
  @close="handleClose"
  class="editor">
 <div class="content">
        <h4>学生答案：</h4>
        <preview :edithtml="clicksubmit.report" :files="clicksubmit.files" :reverse="true"></preview>
        <h4>批语：</h4>
        <el-input
          type="textarea"
          placeholder="请输入内容"
          v-model="clicksubmit.piyu"
          maxlength="200"
          show-word-limit
          autosize
        >
        </el-input>
      </div>
      <div class="addgrade">
          <el-form
            :model="clicksubmit"
            :rules="FormRules"
            ref="FormRef"
            label-width="55px"
            @submit.native.prevent
          >
            <el-form-item label="得分" prop="grade">
              <el-input v-model.number="clicksubmit.grade" ref="gradeInput"></el-input>
            </el-form-item>
          </el-form>
        </div>
  <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="finish">确 定</el-button>
  </span>
</el-dialog>
  </div>
</template>

<script>
import { SEARCHSUBMITLIST ,SUBMITGRADE} from "@/network/teacher";
import { GETPROJECTINFO } from "@/network/teacher";
import Preview from "../common/preview";
export default {
  name: "",
  components: {
    Preview,
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
      projectrecord: [],
      project: {},
      querytype: "all",
      EXPID: "",
      clicksubmit:{},
      row:'',
      dialogVisible:false,
      title:'',
       FormRules: {
        grade: [
          { required: true, message: "请输入分数", trigger: "blur" },
          { type: "number", message: "得分必须为数字值", trigger: "blur" },
          { validator: checkvalue, trigger: "blur" },
        ],
      },
    };
  },
  created() {
    this.EXPID = window.sessionStorage.getItem("EXPID");
  },
  mounted() {
    GETPROJECTINFO(this.EXPID)
      .then((res) => {
        this.project = res.data.project;
        return;
      })
      .then(() => {
        this.search();
      });
  },
  methods: {
    goBack() {
      window.sessionStorage.removeItem("EXPID");
      this.$router.push({ path: "/home/projects" });
    },
    search() {
      SEARCHSUBMITLIST(this.EXPID, this.querytype).then((res) => {
        this.projectrecord = res.data.submitlist;
      });
    },
    addans() {
      this.$router.push({ path: "/home/addanswer" });
    },
    correctall() {
      this.$router.push({ path: "/home/correcting" });
    },
    piyue(row){
      this.row=row;
      this.clicksubmit=JSON.parse(JSON.stringify(row));
      this.dialogVisible=true;
      this.title="批阅报告"
    },
    edit(row){
      this.row=row;
      this.clicksubmit=JSON.parse(JSON.stringify(row));
      this.dialogVisible=true;
      this.title="修改信息"

    },
    handleClose(){
      this.clicksubmit={};
       this.$refs.FormRef.resetFields();
    },
     finish(){
       this.$refs.FormRef.validate(valid=>{
              if(!valid) return;
          SUBMITGRADE(this.clicksubmit).then(res=>{
            let status = res.data.status;
          if (status == "success") {
            this.$message({
              message: "保存成功",
              type: "success",
              duration: 2000,
            });
            // this.row.grade=this.clicksubmit.grade;
            // this.row.piyu=this.clicksubmit.piyu;
            // if(this.row.status=='1'){
            //   this.row.status=='2';
            //   this.clicksubmit.status='2';
            // }
                  this.search();
      this.dialogVisible=false;

          } else {
            this.$message.error("保存失败");
          }
          })
          })
    }
  },
  watch: {
    querytype(val) {
      this.search();
    },
  },
};
</script>
<style lang='less' scoped>
.projecttable {
  width: 70%;
  margin: 0 auto;
}
.addgrade {
  width: 15%;
  margin-top:30px;
}
</style>