<!--  -->
<template>
  <div id="">
    <el-tabs tab-position="left" @tab-click="clearpwd">
      <el-tab-pane label="个人信息" v-if="type==1">
        <el-row>
          <el-col :span="3" :offset="4">学号：</el-col>
          <el-col :span="16"
            ><div>{{ personinfo.STID }}</div></el-col
          >
        </el-row>
        <el-row>
          <el-col :span="3" :offset="4">姓名：</el-col>
          <el-col :span="16"
            ><div>{{ personinfo.name }}</div></el-col
          >
        </el-row>
        <el-row>
          <el-col :span="3" :offset="4">班级：</el-col>
          <el-col :span="16"
            ><div>{{ personinfo.classno }}</div></el-col
          >
        </el-row>
        <el-row>
          <el-col :span="3" :offset="4">任课老师：</el-col>
          <el-col :span="16"
            ><div>{{ personinfo.teacher }}</div></el-col
          >
        </el-row>
      </el-tab-pane>
      <el-tab-pane label="个人信息" v-if="type==2">
        <el-row>
          <el-col :span="3" :offset="4">教职号：</el-col>
          <el-col :span="16"
            ><div>{{ personinfo.TEID }}</div></el-col
          >
        </el-row>
        <el-row>
          <el-col :span="3" :offset="4">姓名：</el-col>
          <el-col :span="16"
            ><div>{{ personinfo.name }}</div></el-col
          >
        </el-row>
        <el-row>
          <el-col :span="3" :offset="4">任教班级：</el-col>
          <el-col :span="16"
            ><div>{{ classnolist.join(",") }}</div></el-col
          >
        </el-row>

        <el-form
          :model="personinfo"
          :rules="editPwdRules"
          ref="editInfoFormRef"
          label-width="85px"
        >
          <el-form-item label="联系方式:" prop="phonenum">
            <el-input
              v-model="personinfo.phonenum"
              style="width: 70%; margin-right: 10%"
            ></el-input>
            <el-button
              type="primary"
              icon="el-icon-edit"
              size="mini"
              @click="editinfo"
            ></el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="修改密码">
        <el-form
          :model="editpwd"
          :rules="editPwdRules"
          ref="editpwdFormRef"
          label-width="80px"
        >
          <el-form-item label="新密码" prop="newpwd">
            <el-input v-model="editpwd.newpwd" type="password"></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="checkpwd">
            <el-input v-model="editpwd.checkpwd" type="password"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="editpassword(role)">确定</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import {
  EDITPWD,
  GETINFO,
  SETINFO,
SEARCH
} from "@/network/management";
import { GETCLASSLIST } from "@/network/teacher";
export default {
  name: "",
  data() {
    var checkpassword = (rule, value, cb) => {
      if (value === this.editpwd.newpwd) {
        return cb();
      }
      cb(new Error("两次密码输入不一致"));
    };
    //验证手机号
    var checkMobile = (rule, value, cb) => {
      const regMobile = /^[1](([3][0-9])|([4][0,1,4-9])|([5][0-3,5-9])|([6][2,5,6,7])|([7][0-8])|([8][0-9])|([9][0-3,5-9]))[0-9]{8}$/;

      if (regMobile.test(value)) {
        return cb();
      }
      cb(new Error("请输入合法手机号"));
    };
    return {
      personinfo: {        
      },
      classnolist: [],
      username:'',
      type:'',
      role:'',
      editpwd: {
        newpwd: "",
        checkpwd: "",
      },
      editPwdRules: {
        newpwd: [
          { required: true, message: "请输入新密码", trigger: "blur" },
          {
            min: 6,
            max: 15,
            message: "密码的长度在6-15个字符之间",
            trigger: "blur",
          },
        ],
        checkpwd: [
          { required: true, message: "请再次输入密码", trigger: "blur" },
          { validator: checkpassword, trigger: "blur" },
        ],
        phonenum: [
          { required: true, message: "请输入手机号", trigger: "blur" },
          { validator: checkMobile, trigger: "blur" },
        ],
      },
    };
  },
  created() {
    this.username=window.sessionStorage.getItem("username");
    this.type=window.sessionStorage.getItem("type");
  },
  mounted() {
    if(this.type==2){
      this.role='teacher';
    GETCLASSLIST(this.username).then((res) => {
      this.classnolist = res.data.data;
      return;
    }).then(()=>{
      this.getinfo('teacher');
      
    })}else{
      this.role='student';
      GETINFO(this.username,'student').then(res=>{
        this.personinfo=res.data.data;
        return this.personinfo.classno.toString();
      }).then((classno)=>{
        SEARCH(classno,'classno','class',false).then(res=>{
          this.$set(this.personinfo,'teacher',res.data.data[0].teacher)
        })
      })
    }
   
  },
  methods: {
    clearpwd(item) {
      if (item.index == 0) {
        this.$refs.editpwdFormRef.resetFields();
        if(this.type==2){
        this.getinfo('teacher');
        }
      } else if (item.index == 1) {
        if(this.type==2){
        
        this.$refs.editInfoFormRef.resetFields();
        }
      }
    },
    getinfo(role){
      GETINFO(this.username,role).then(res=>{
        this.personinfo=res.data.data;
      })
    },
    editinfo(){
      
      this.$refs.editInfoFormRef.validate((valid) => {
        if (!valid) return;
        SETINFO(
          this.username,
          this.personinfo.phonenum,
          "teacher"
        ).then((res) => {
          let msg = res.data.status;
          if (msg == "success") {
            this.$message({
              message: "修改成功",
              type: "success",
              duration: 2000,
            });
            this.getinfo('teacher');
          } else if (msg == "fail") {
            this.$message.error("修改失败");
          }
        });
      });
    },
    editpassword(role){
        this.$refs.editpwdFormRef.validate((valid) => {
        if (!valid) return;
        EDITPWD(this.username, this.editpwd.checkpwd, role).then(
          (res) => {
            let msg = res.data.status;
            if (msg == "success") {
              this.$message({
                message: "修改成功",
                type: "success",
                duration: 2000,
              });
              this.$refs.editpwdFormRef.resetFields();
            } else if (msg == "fail") {
              this.$message.error("修改失败");
            }
          }
        );
      });
    }
  },
};
</script>
<style lang='less' scoped>
.el-tabs {
  height: 50vh;
  width: 50%;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
.el-row {
  margin-top: 30px;
  margin-bottom: 30px;
}
.el-form {
  margin-left: 14.67%;
  width: 50%;
  margin-top: 30px;
}
</style>