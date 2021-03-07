<!--  -->
<template>
  <div id="">
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home/classes' }"
        >班级管理</el-breadcrumb-item
      >
      <el-breadcrumb-item>班级列表</el-breadcrumb-item>
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
              <el-option label="班级号" value="classno"></el-option>
              <el-option label="任课老师" value="teacher"></el-option>
            </el-select>
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="search"
            ></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="addclass">添加班级</el-button>
        </el-col>
      </el-row>
      <el-table :data="classlist" border height="60vh">
        <el-table-column prop="currentid" align="center" width="50px">
        </el-table-column>
        <el-table-column prop="classno" label="班级号" > </el-table-column>
        <el-table-column prop="teacher" label="任课老师" > </el-table-column>
        <el-table-column prop="peoplenum" label="人数" ></el-table-column>
        <el-table-column label="操作">
          <template v-slot="scope">
            <el-tooltip
              effect="dark"
              content="选择任课老师"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="primary"
                icon="el-icon-user-solid"
                size="mini"
                @click="editInfo(scope.row.classno)"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              effect="dark"
              content="删除"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="danger"
                icon="el-icon-delete"
                size="mini"
                @click="del(scope.row.classno)"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @current-change="handleCurrentChange"
        :current-page="queryInfo.pagenum"
        :page-size="20"
        layout="total, prev, pager, next"
        :total="total"
      >
      </el-pagination>
    </el-card>
    <!-- 删除用户 -->
    <el-dialog
      title="删除班级"
      :visible.sync="DialogVisible.delDialogVisible"
      width="30%"
    >
      <span>是否确定<span class="deltip">删除</span>该班级?</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible.delDialogVisible = false"
          >取 消</el-button
        >
        <el-button type="primary" @click="delclass">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 修改信息 -->
    <el-dialog
      title="选择任课老师"
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
        <el-form-item label="教师身份" prop="teacher">
          <el-autocomplete
            v-model="editInfoForm.teacher"
            :fetch-suggestions="querySearchAsync"
            placeholder="请输入姓名或教职号"
          ></el-autocomplete>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible.editinfoDialogVisible = false"
          >取 消</el-button
        >
        <el-button type="primary" @click="editclassinfo">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 添加班级 -->
    <el-dialog
      title="添加班级"
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
        <el-form-item label="班级号" prop="classno">
          <el-input v-model.number="addUserForm.classno"></el-input>
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
        <el-button type="primary" @click="addclassinfo">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { debounce } from "@/common/utils";
import { DEL, SEARCH, GETINFO, SETINFO, ADDCLASS } from "@/network/management";
export default {
  name: "",
  data() {
    //检验长度
    var checklen = (rule, value, callback) => {
      if (value) {
        if ((value + "").length !== 6) {
          callback(new Error("班级号长度必须为6个数字"));
        } else {
          callback();
        }
      }
      callback();
    };
    return {
      queryInfo: {
        query: "",
        pagenum: 1,
        querytype: "queryall",
        pagesize: 20,
      },
      classlist: [],
      total: 0,
      DialogVisible: {
        delDialogVisible: false,
        editinfoDialogVisible: false,
        adduserDialogVisible: false,
      },

      editInfoForm: {},
      addUserForm: {
        classno: "",
        teacher: "",
      },
      editFormRules: {
        classno: [
          { required: true, message: "请输入班级号", trigger: "blur" },
          { type: "number", message: "班级号必须为数字值", trigger: "blur" },
          { validator: checklen, trigger: "blur" },
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
    // this.search();
    // setTimeout(() => {
    //   this.getteachers();
    // }, 1000);
    SEARCH(
        this.queryInfo.query,
        this.queryInfo.querytype,
        "class",
        false
      ).then((res) => {
        this.datalist = res.data.data;
        this.total = this.datalist.length;
        this.classlist = this.datalist.slice(
          this.queryInfo.pagesize * (this.queryInfo.pagenum - 1),
          this.queryInfo.pagesize * this.queryInfo.pagenum
        );
        return;
      }).then(()=>{
        this.getteachers();
      });
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
      this.classlist = this.datalist.slice(
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
        "class",
        loading
      ).then((res) => {
        this.datalist = res.data.data;
        this.total = this.datalist.length;
        this.classlist = this.datalist.slice(
          this.queryInfo.pagesize * (this.queryInfo.pagenum - 1),
          this.queryInfo.pagesize * this.queryInfo.pagenum
        );
      });
    },

    del(username) {
      this.clickusername = username;
      this.DialogVisible.delDialogVisible = true;
    },
    delclass() {
      DEL(this.clickusername, "class").then((res) => {
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
    editInfo(username) {
      GETINFO(username, "class").then((res) => {
        this.editInfoForm = res.data.data;
        this.clickusername = username;
        this.DialogVisible.editinfoDialogVisible = true;
      });
    },
    editclassinfo() {
      this.$refs.editFormRef.validate((valid) => {
        if (!valid) return;
        SETINFO(
          this.clickusername,
          this.editInfoForm.teacher.split("---")[1],
          "class"
        ).then((res) => {
          let msg = res.data.status;
          if (msg == "no teacher") {
            this.$message.error("该教师不存在");
          } else if (msg == "success") {
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
    addclass() {
      this.DialogVisible.adduserDialogVisible = true;
    },
    addclassinfo() {
      this.$refs.addFormRef.validate((valid) => {
        if (!valid) return;
        // console.log(this.addUserForm.username,this.addUserForm.checkaddpassword,this.addUserForm.teacher.split('---')[1])
        ADDCLASS(
          this.addUserForm.classno,
          this.addUserForm.teacher.split("---")[1],
          true
        ).then((res) => {
          let msg = res.data.status;
          console.log(msg);
          if (msg == "has classno") {
            this.$message.error("该班级号已存在");
          } else if (msg == "no teacher") {
            this.$message.error("该教师不存在");
          } else if (msg == "success") {
            this.$message({
              message: "添加班级成功",
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