<!--  -->
<template>
  <div id="">
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home/admins' }"
        >管理员管理</el-breadcrumb-item
      >
      <el-breadcrumb-item>管理员列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-row :gutter="20">
        <el-col :span="10">
          <el-input
            placeholder="请输入内容"
            class="input-with-select"
            ref="searchInput"
            v-model="queryInfo.query"
          >
            <el-select v-model="queryInfo.querytype" slot="prepend">
              <el-option label="综合" value="queryall"></el-option>
              <el-option label="账号" value="username"></el-option>
              <el-option label="姓名" value="name"></el-option>
              <el-option label="联系方式" value="phonenum"></el-option>
              <el-option label="教职号" value="TEID"></el-option>
            </el-select>
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="search"
            ></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="adduser">添加用户</el-button>
        </el-col>
      </el-row>
      <el-table :data="userlist" border height="60vh">
        <el-table-column prop="currentid" align="center" width="50px">
        </el-table-column>
        <el-table-column prop="username" label="账号"> </el-table-column>
        <el-table-column prop="name" label="姓名"> </el-table-column>
        <el-table-column prop="phonenum" label="联系方式"> </el-table-column>
        <el-table-column prop="TEID" label="教职号"> </el-table-column>
        <el-table-column label="操作">
          <template v-slot="scope">
            <el-tooltip
              effect="dark"
              content="编辑信息"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="mini"
                @click="editInfo(scope.row.username)"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              effect="dark"
              content="重置密码"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="success"
                icon="el-icon-refresh-left"
                size="mini"
                @click="reset(scope.row.username)"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              v-if="scope.row.username != 'admin'"
              effect="dark"
              content="删除"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="danger"
                icon="el-icon-delete"
                size="mini"
                @click="del(scope.row.username)"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              v-if="scope.row.username === currentuser"
              effect="dark"
              content="修改密码"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="warning"
                icon="el-icon-user-solid"
                size="mini"
                @click="editpwd(scope.row.username)"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @current-change="handleCurrentChange"
        :current-page="queryInfo.pagenum"
        :page-size="queryInfo.pagesize"
        layout="total, prev, pager, next"
        :total="total"
      >
      </el-pagination>
    </el-card>
    <!-- 删除用户 -->
    <el-dialog
      title="删除用户"
      :visible.sync="DialogVisible.delDialogVisible"
      width="30%"
    >
      <span>是否确定<span class="deltip">删除</span>该用户?</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible.delDialogVisible = false"
          >取 消</el-button
        >
        <el-button type="primary" @click="deladmin">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 重置密码 -->
    <el-dialog
      title="重置密码"
      :visible.sync="DialogVisible.resetDialogVisible"
      width="30%"
    >
      <span>是否确定<span class="Btip">重置</span>该用户密码?</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible.resetDialogVisible = false"
          >取 消</el-button
        >
        <el-button type="primary" @click="resetPWD">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 修改密码 -->
    <el-dialog
      title="修改密码"
      :visible.sync="DialogVisible.editpwdDialogVisible"
      width="30%"
      @close="editpwdDialogClosed"
    >
      <el-form
        :model="editForm"
        :rules="editFormRules"
        ref="editpwdFormRef"
        label-width="80px"
      >
        <el-form-item label="新密码" prop="newpwd">
          <el-input v-model="editForm.newpwd" type="password"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkpwd">
          <el-input v-model="editForm.checkpwd" type="password"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible.editpwdDialogVisible = false"
          >取 消</el-button
        >
        <el-button type="primary" @click="editpassword">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 修改信息 -->
    <el-dialog
      title="修改信息"
      :visible.sync="DialogVisible.editinfoDialogVisible"
      width="30%"
      @close="editinfoDialogClosed"
    >
      <el-form
        :model="editInfoForm"
        :rules="editFormRules"
        ref="editFormRef"
        label-width="80px"
      >
        <el-form-item label="账号">
          <el-input v-model="editInfoForm.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="editInfoForm.name" disabled></el-input>
        </el-form-item>
        <el-form-item label="教职号">
          <el-input v-model="editInfoForm.TEID" disabled></el-input>
        </el-form-item>
        <el-form-item label="联系方式" prop="phonenum">
          <el-input v-model="editInfoForm.phonenum"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible.editinfoDialogVisible = false"
          >取 消</el-button
        >
        <el-button type="primary" @click="edituserinfo">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 添加管理员 -->
    <el-dialog
      title="添加用户"
      :visible.sync="DialogVisible.adduserDialogVisible"
      width="30%"
      @close="adduserDialogClosed"
    >
      <el-form
        :model="addUserForm"
        :rules="editFormRules"
        ref="addFormRef"
        label-width="90px"
      >
        <el-form-item label="账号" prop="username">
          <el-input v-model="addUserForm.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="addUserForm.password"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkaddpassword">
          <el-input
            type="password"
            v-model="addUserForm.checkaddpassword"
          ></el-input>
        </el-form-item>
        <el-form-item label="教师身份" prop="teacher">
          <el-autocomplete
            v-model="addUserForm.teacher"
            :fetch-suggestions="querySearchAsync"
            placeholder="请输入姓名或教职号"
          ></el-autocomplete>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible.adduserDialogVisible = false"
          >取 消</el-button
        >
        <el-button type="primary" @click="addadmin">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { debounce } from "@/common/utils";
import {
  RESETPWD,
  DEL,
  EDITPWD,
  SEARCH,
  GETINFO,
  SETINFO,
  ADDADMIN,
} from "@/network/management";
export default {
  name: "",
  data() {
    //验证密码一致
    var checkpassword = (rule, value, cb) => {
      if (value === this.editForm.newpwd) {
        return cb();
      }
      cb(new Error("两次密码输入不一致"));
    };
    var checkaddpwd = (rule, value, cb) => {
      if (value === this.addUserForm.password) {
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
    var checkDigit = (rule, value, cb) => {
      const regDight = /^[\d]*$/;

      if (regDight.test(value)) {
        return cb(new Error("账号不能由纯数字组成"));
      }
      cb();
    };
    return {
      queryInfo: {
        query: "",
        pagenum: 1,
        querytype: "queryall",
        pagesize: 20,
      },
      userlist: [],
      total: 0,
      DialogVisible: {
        delDialogVisible: false,
        resetDialogVisible: false,
        editpwdDialogVisible: false,
        editinfoDialogVisible: false,
        adduserDialogVisible: false,
      },
      editForm: {
        newpwd: "",
        checkpwd: "",
      },
      editInfoForm: {
        username: "admin",
        name: "zhy",
        phonenum: "17376594388",
        TEID: "2010050501",
      },
      addUserForm: {
        username: "",
        password: "",
        teacher: "",
        checkaddpassword: "",
      },
      editFormRules: {
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
        checkaddpassword: [
          { required: true, message: "请再次输入密码", trigger: "blur" },
          { validator: checkaddpwd, trigger: "blur" },
        ],
        phonenum: [
          { required: true, message: "请输入手机号", trigger: "blur" },
          { validator: checkMobile, trigger: "blur" },
        ],
        username: [
          { required: true, message: "请输入账号", trigger: "blur" },
          {
            min: 5,
            max: 15,
            message: "账号的长度在5-15个字符之间",
            trigger: "blur",
          },
          { validator: checkDigit, trigger: "blur" },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          {
            min: 6,
            max: 15,
            message: "密码的长度在6-15个字符之间",
            trigger: "blur",
          },
        ],
        teacher: [
          {
            required: true,
            message: "请输入教师身份",
            trigger: ["blur", "change"],
          },
        ],
      },
      search: "",
      currentuser: "",
      clickusername: "",
      datalist: [],
      teacherlist: [],
    };
  },
  created() {
    this.currentuser = window.sessionStorage.getItem("username");
  },
  mounted() {
    window.addEventListener("keydown", this.keyDown);
    this.search = debounce(this.searchInfo, 500, true);
    // this.search().then(()=>{
    //   this.getteachers();
    // });
    // setTimeout(() => {
    //   this.getteachers();
    // }, 1000);
     SEARCH(
        this.queryInfo.query,
        this.queryInfo.querytype,
        "admin",
        false
      ).then((res) => {
        this.datalist = res.data.data;
        this.total = this.datalist.length;
        this.userlist = this.datalist.slice(
          this.queryInfo.pagesize * (this.queryInfo.pagenum - 1),
          this.queryInfo.pagesize * this.queryInfo.pagenum
        );
        return;
      }).then(()=>{
        this.getteachers();
      })
  },
  methods: {
    getteachers() {
      SEARCH("", "queryall", "teacher").then((res) => {
        let teachers = res.data.data;
        teachers.forEach((item) => {
          let temp = {};
          temp["value"] = item.teacher;
          temp["TEID"] = item.TEID;
          this.teacherlist.push(temp);
        });
      });
    },
    keyDown(e) {
      if (e.keyCode == 13 && this.$refs.searchInput.focused == true) {
        this.search();
      }
    },
    handleCurrentChange(val) {
      this.queryInfo.pagenum = val;
      this.userlist = this.datalist.slice(
        this.queryInfo.pagesize * (this.queryInfo.pagenum - 1),
        this.queryInfo.pagesize * this.queryInfo.pagenum
      );
    },
    searchInfo(loading = false, clear = true) {
      if (this.queryInfo.query != "" && clear) {
        this.queryInfo.pagenum = 1;
      }
      SEARCH(
        this.queryInfo.query,
        this.queryInfo.querytype,
        "admin",
        loading
      ).then((res) => {
        this.datalist = res.data.data;
        this.total = this.datalist.length;
        this.userlist = this.datalist.slice(
          this.queryInfo.pagesize * (this.queryInfo.pagenum - 1),
          this.queryInfo.pagesize * this.queryInfo.pagenum
        );
      });
    },
    reset(username) {
      this.clickusername = username;
      this.DialogVisible.resetDialogVisible = true;
    },
    resetPWD() {
      RESETPWD(this.clickusername).then((res) => {
        let msg = res.data.status;
        if (msg == "success") {
          this.$message({
            message: "重置成功,密码为身份证后6位",
            type: "success",
            duration: 2000,
          });
          this.DialogVisible.resetDialogVisible = false;
        } else if (msg == "fail") {
          this.$message.error("重置失败");
        } else if (msg == "No user") {
          this.$message.error("该用户不存在");
        }
      });
    },
    del(username) {
      this.clickusername = username;
      this.DialogVisible.delDialogVisible = true;
    },
    deladmin() {
      DEL(this.clickusername, "admin").then((res) => {
        let msg = res.data.status;
        if (msg == "success") {
          this.$message({
            message: "删除成功",
            type: "success",
            duration: 2000,
          });
          this.DialogVisible.delDialogVisible = false;
          this.searchInfo(true, false);
        } else if (msg == "fail") {
          this.$message.error("删除失败");
        }
      });
    },
    editpwd(username) {
      this.clickusername = username;
      this.DialogVisible.editpwdDialogVisible = true;
    },
    editpassword() {
      this.$refs.editpwdFormRef.validate((valid) => {
        if (!valid) return;
        EDITPWD(this.clickusername, this.editForm.checkpwd, "admin").then(
          (res) => {
            let msg = res.data.status;
            if (msg == "success") {
              this.$message({
                message: "修改成功",
                type: "success",
                duration: 2000,
              });
              this.DialogVisible.editpwdDialogVisible = false;
            } else if (msg == "fail") {
              this.$message.error("修改失败");
            }
          }
        );
      });
    },
    editInfo(username) {
      GETINFO(username, "admin").then((res) => {
        this.editInfoForm = res.data.data;
        this.DialogVisible.editinfoDialogVisible = true;
      });
    },
    edituserinfo() {
      this.$refs.editFormRef.validate((valid) => {
        if (!valid) return;
        SETINFO(
          this.editInfoForm.username,
          this.editInfoForm.phonenum,
          "admin"
        ).then((res) => {
          let msg = res.data.status;
          if (msg == "success") {
            this.$message({
              message: "修改成功",
              type: "success",
              duration: 2000,
            });
            this.DialogVisible.editinfoDialogVisible = false;
            this.searchInfo(true, false);
          } else if (msg == "fail") {
            this.$message.error("修改失败");
          }
        });
      });
    },
    adduser() {
      this.DialogVisible.adduserDialogVisible = true;
    },
    addadmin() {
      this.$refs.addFormRef.validate((valid) => {
        if (!valid) return;
        // console.log(this.addUserForm.username,this.addUserForm.checkaddpassword,this.addUserForm.teacher.split('---')[1])
        ADDADMIN(
          this.addUserForm.username,
          this.addUserForm.checkaddpassword,
          this.addUserForm.teacher.split("---")[1],
          true
        ).then((res) => {
          let msg = res.data.status;
          if (msg == "no teacher") {
            this.$message.error("不存在该教师");
          } else if (msg == "has account") {
            this.$message.error("该账号已存在");
          } else if (msg == "has signed") {
            this.$message.error("该教师已拥有管理员身份");
          } else if (msg == "success") {
            this.$message({
              message: "添加用户成功",
              type: "success",
              duration: 2000,
            });
            this.DialogVisible.adduserDialogVisible = false;
            this.searchInfo(true, false);
          } else if (msg == "fail") {
            this.$message.error("添加失败");
          }
        });
      });
    },
    // 退出时清除表单内容
    editpwdDialogClosed() {
      this.$refs.editpwdFormRef.resetFields();
    },
    editinfoDialogClosed() {
      this.$refs.editFormRef.resetFields();
    },
    adduserDialogClosed() {
      // this.addUserForm.teacher='';
      this.$refs.addFormRef.resetFields();
    },
    //动态搜索老师
    querySearchAsync(queryString, cb) {
      var teacherlist = this.teacherlist;
      var result = queryString
        ? teacherlist.filter(this.createStateFilter(queryString))
        : teacherlist;
      cb(result);
    },
    createStateFilter(queryString) {
      return (state) => {
        return (
          state.value.toLowerCase().indexOf(queryString.toLowerCase()) >= 0
        );
      };
    },
  },
  destroyed() {
    window.removeEventListener("keydown", this.keyDown, false);
  },
};
</script>
<style lang='less' scoped>
.el-form {
  width: 80%;
  margin: 0 auto;
}
</style>