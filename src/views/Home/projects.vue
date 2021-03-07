<!--  -->
<template>
  <div id="project">
    <div class="head">
      <div class="radio" v-if="type==1">
        <span style="color: #606266">筛选：</span>
        <el-radio-group v-model="querytype">
          <el-radio label="all">全部</el-radio>
          <el-radio label="waitcorrect">待批阅</el-radio>
          <el-radio label="finished">已完成</el-radio>
          <el-radio label="unfinished">未完成</el-radio>
        </el-radio-group>
      </div>
      <div class="radio" v-if="type==2">
        <span style="color: #606266">我发布的：</span>
        <el-radio-group v-model="querytype">
          <el-radio label="all">全部</el-radio>
          <!-- <el-radio label="finished">已完成</el-radio>
      <el-radio label="unfinished">未完成</el-radio> -->
          <el-radio
            v-for="(classno, index) in classnolist"
            v-bind:key="index"
            :label="classno"
          >
            {{ classno }}
          </el-radio>
        </el-radio-group>
      </div>
      <div class="info" v-if="type==1">
        <span>{{
          "班级：" + (info.classno == "" ? "暂无信息" : info.classno)
        }}</span>
        <el-divider direction="vertical"></el-divider>
        <span>{{
          "任课老师：" + (info.teacher == "" ? "暂无信息" : info.teacher)
        }}</span>
      </div>
      <div class="addproject" v-if="type==2">
         <el-button type="primary" @click="addproject">发布实验项目</el-button>
      </div>
      <el-divider></el-divider>
    </div>
    <!-- 学生端 -->
    <el-row class="el-row" :gutter="30" v-if="type==1">
      <el-col v-for="(item, index) in projectlist" v-bind:key="index" :span="6">
        <el-card shadow="hover" class="project">
          <div
            slot="header"
            class="clearfix"
            @click="gotodetail(item.recordID, item.EXPID,item.isread,item.status)"
          >
            <el-badge :is-dot="!item.isread" class="title">{{
              item.title
            }}</el-badge>
          </div>
          <div class="item">
            {{ "开始时间：" + item.start }}
          </div>
          <div class="item">
            {{ "截止时间：" + item.end }}
          </div>
          <div class="item">
            <span>状态：</span>
            <span
              class="ball"
              :style="{ background: getcolor(item.status) }"
            ></span>
            <span>{{ getstatus(item.status) }}</span>
          </div>

          <el-button
            @click="gotodetail(item.recordID, item.EXPID,item.isread,item.status)"
            style="float: right"
            type="info"
            size="mini"
            icon="el-icon-s-order"
            >查看详情</el-button
          >
        </el-card>
      </el-col>
    </el-row>
    <!-- 教师端 -->
    <el-row class="el-row" :gutter="30" v-if="type==2">
      <el-col v-for="(item, index) in projectlist" v-bind:key="index" :span="6">
        <el-card shadow="hover" class="project">
          <div
            slot="header"
            class="clearfix"
          >
            <div class="title">{{item.title}}</div>
          </div>
          <div class="item">
            {{ "开始时间：" + item.start }}
          </div>
          <div class="item">
            {{ "截止时间：" + item.end }}
          </div>
          <div class="item">
            <span>状态：</span>
            <span
              class="ball"
              :style="{ background: getcolor(item.issub) }"
            ></span>
            <span >{{ getstatus(item.issub) }}</span>
            <div class="pubclass">
            <span>发布班级：</span>
            <span>{{ item.classno }}</span>
            </div>
          </div>
          <div class="item under">
            <span>
              <span>上交人数：</span>
              <span class="colorred">{{item.subnum}}</span>
              <span>/</span>
              <span>{{item.totalnum}}</span>
            </span>
         <el-button-group class="pubclass">
           <el-tooltip content="编辑" placement="top">
  <el-button type="info" size="mini" icon="el-icon-edit" @click="editproject(item.EXPID)"></el-button>
           </el-tooltip>
           <el-tooltip content="详情" placement="top">
  <el-button type="info" size="mini" icon="el-icon-tickets" @click="correctproject(item.EXPID)"></el-button>
           </el-tooltip>

           <el-tooltip content="删除" placement="top">
  <el-button type="info" size="mini" icon="el-icon-delete" @click="delproject(item.EXPID)"></el-button>
           </el-tooltip>
</el-button-group>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <!-- 删除项目 -->
     <el-dialog
      title="删除实验项目"
      :visible.sync="deletevisible"
      width="30%"
    >
      <span>是否确定<span class="deltip">删除</span>该实验项目?</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deletevisible = false"
          >取 消</el-button
        >
        <el-button type="primary" @click="delprj">确 定</el-button>
      </span>
    </el-dialog>
  </div>
  
</template>

<script>
import {GETCLASSLIST,SEARCHPROJECT,DELPROJECT} from '@/network/teacher';
import {GETBASICINFO,READPROJECTINFO} from '@/network/student';
import { formatDate } from "@/common/utils";
export default {
  name: "",
  data() {
    return {
      projectlist: [

      ],
      querytype: "all",
      info: {
        classno: "201701",
        teacher: "朱海燕",
      },
      type:-1,
      username:'',
      classnolist: [],
      deletevisible:false,
      clickEXPID:''
    };
  },
  computed: {
    getcolor() {
      return function (val) {
        if (val == "1") {
          return "#cccccc";
        } else if (val == "2") {
          return "#FFA500";
        } else if (val == "3") {
          return "#00ff00";
        } else if (val == "4") {
          return "#FF0000";
        }else if (val == "5") {
          return "#FFA500";
        } else if (val == "6") {
          return "#00ff00";
        }
      };
    },
    getstatus() {
      return function (val) {
        if (val == "1") {
          return "未完成";
        } else if (val == "2") {
          return "待批阅";
        } else if (val == "3") {
          return "已完成";
        } else if (val == "4") {
          return "已超时";
        }else if(val=="5"){
          return "待发布"
        }else if(val=="6"){
          return "已发布"
        }
      };
    },
  },
  created() {
    // console.log(formatDate(new Date(),'YYYY-MM-dd hh:mm:ss'))
    this.type=window.sessionStorage.getItem('type')
    this.username=window.sessionStorage.getItem('username')
  },
  mounted() {
    if(this.type==2){
      GETCLASSLIST(this.username).then(res=>{
        this.classnolist=res.data.data
        return this.classnolist
      }).then((res)=>{
        this.search()
      })
    }else if(this.type==1){
      GETBASICINFO(this.username).then(res=>{
        this.info=res.data.data
        return ''
      }).then(()=>{
        this.search(false,"studentproject")
      })
    }
  },
  methods: {
    gotodetail(recordID,EXPID,isread,status) {
      //已读 1后再跳转 .then
      if(isread==1){
         window.sessionStorage.setItem("EXPID", EXPID);
      window.sessionStorage.setItem("recordID", recordID);
      window.sessionStorage.setItem('status',status);
      this.$router.push({ path: "/home/detail" });
      }else{
        READPROJECTINFO(recordID).then(()=>{
           window.sessionStorage.setItem("EXPID", EXPID);
      window.sessionStorage.setItem("recordID", recordID);
      window.sessionStorage.setItem('status',status);
      this.$router.push({ path: "/home/detail" });
        })

      }

    
    },
    search(loading = false,projecttype="teacherproject") {
      SEARCHPROJECT(this.querytype,this.username,projecttype,loading).then(res=>{
        this.projectlist=res.data.data
      })
    },
    delproject(EXPID){
      this.clickEXPID=EXPID
       this.deletevisible=true
    },
    delprj(){
      DELPROJECT(this.clickEXPID).then(res=>{
        let status=res.data.status
          if(status=="success"){
             this.$message({
            message: "删除成功",
            type: "success",
            duration: 2000,
          });
          this.search();
          this.deletevisible=false
          }else{
            this.$message.error("删除失败");
          }
      })
    },
    editproject(EXPID){
      window.sessionStorage.setItem("EXPID", EXPID);
      this.$router.push({ path: "/home/editproject" });
    },
    correctproject(EXPID){
      window.sessionStorage.setItem("EXPID", EXPID);
      this.$router.push({ path: "/home/correctproject" });
    },
    addproject(){
      this.$router.push({ path: "/home/addproject" });
    }
  },
  watch: {
    querytype(val) {
      if(this.type==2){
        this.search();
      }else{
        this.search(false,"studentproject")
      }
    },
  },
};
</script>
<style lang='less' scoped>
.el-col {
  height: 30vh;
  margin-bottom: 30px;
}

.el-card {
  height: 100%;
  min-height: 100%;
}
.el-card > .el-card__body {
  height: 100%;
}
.title {
  display: -webkit-box; /*作为弹性伸缩盒子模型显示*/
  -webkit-line-clamp: 1; /*显示的行数；如果要设置2行加...则设置为2*/
  overflow: hidden; /*超出的文本隐藏*/
  text-overflow: ellipsis; /* 溢出用省略号*/
  -webkit-box-orient: vertical; /*伸缩盒子的子元素排列：从上到下*/
  font-weight: 700;
  cursor: pointer;
}
.title:hover {
  color: #606266;
}
.head {
  position: relative;
}
.info {
  position: absolute;
  right: 0;
  top: 0;
  color: #606266;
}
.item {
  margin-bottom: 15px;
  font-size: 14px;
  color: #606266;
  white-space: nowrap;
}
.ball {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 6px;
}
.addproject{
  position: absolute;
  right:0;
  top:-25%;
}
.pubclass{
  float:right
}
.colorred{
  color:red;
}
.under{
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>