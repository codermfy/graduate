<!--  -->
<template>
  <div id="">
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home/teachers' }"
        >教师管理</el-breadcrumb-item
      >
      <el-breadcrumb-item>教师列表</el-breadcrumb-item>
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
              <el-option label="教职号" value="TEID"></el-option>
              <el-option label="姓名" value="name"></el-option>
              <el-option label="联系方式" value="phonenum"></el-option>
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
        <el-col :span="3" :offset="7">
          <el-button type="success" @click="addall">批量导入</el-button>
        </el-col>
      </el-row>
      <el-table :data="userlist" border height="60vh">
        <el-table-column prop="currentid" align="center" width="50px">
        </el-table-column>
        <el-table-column prop="TEID" label="教职号"> </el-table-column>
        <el-table-column prop="name" label="姓名"> </el-table-column>
        <el-table-column prop="phonenum" label="联系方式"> </el-table-column>
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
                @click="editInfo(scope.row.TEID)"
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
                @click="reset(scope.row.TEID)"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              v-if="true"
              effect="dark"
              content="删除"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="danger"
                icon="el-icon-delete"
                size="mini"
                @click="del(scope.row.TEID)"
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
      title="删除用户"
      :visible.sync="DialogVisible.delDialogVisible"
      width="30%"
    >
      <span>是否确定<span class="deltip">删除</span>该用户?</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible.delDialogVisible = false"
          >取 消</el-button
        >
        <el-button type="primary" @click="delteacher">确 定</el-button>
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
        <el-form-item label="教职号">
          <el-input v-model="editInfoForm.TEID" disabled></el-input>
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="editInfoForm.name" disabled></el-input>
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
    <!-- 添加用户 -->
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
        <el-form-item label="教职号" prop="TEID">
          <el-input v-model.number="addUserForm.TEID"></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="addUserForm.name"></el-input>
        </el-form-item>
        <el-form-item label="身份证号" prop="cardno">
          <el-input v-model="addUserForm.cardno"></el-input>
        </el-form-item>
        <el-form-item label="联系方式" prop="phonenum">
          <el-input v-model="addUserForm.phonenum"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible.adduserDialogVisible = false"
          >取 消</el-button
        >
        <el-button type="primary" @click="addteacher">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 批量导入 -->
    <el-dialog
      title="批量导入"
      :visible.sync="DialogVisible.allimportDialogVisible"
      width="60%"
      @close="allimportDialogClosed"
    >
      <el-row>
        <el-col :span="4">
          <el-upload
            　　　　action="/"
            　　　　:on-change="uploadChange"
            　　　　:show-file-list="false"
            　　　　accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel"
            　　　　:auto-upload="false"
          >
            　　　　
            <el-button size="small" icon="el-icon-upload" type="primary"
              >导入excel</el-button
            >
            　　
          </el-upload>
        </el-col>
        <el-col :span="4" :offset="16">
          <span>总共有{{ xlsctotal }}条记录</span>
        </el-col>
      </el-row>

      <el-alert
        v-if="!isrepeat"
        title="导入的数据必须是正确合法的才能进行批量添加(教职号唯一、一个身份证号对应一位教师)"
        type="info"
        show-icon
        :closable="false"
      >
      </el-alert>
      <el-alert
        v-if="isrepeat"
        title="导入的数据存在重复记录(教职号重复、身份证号重复)"
        type="error"
        show-icon
        :closable="false"
      >
      </el-alert>
      <el-table :data="xlscList" border height="30vh">
        <el-table-column type="index" align="center"> </el-table-column>
        <el-table-column prop="TEID" label="教职号"> </el-table-column>
        <el-table-column prop="name" label="姓名"> </el-table-column>
        <el-table-column prop="phonenum" label="联系方式"> </el-table-column>
        <el-table-column prop="cardno" label="身份证号"> </el-table-column>
      </el-table>

      <span slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible.allimportDialogVisible = false"
          >取 消</el-button
        >
        <el-button type="primary" @click="addteacherbyfile">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { debounce, file2Xce } from "@/common/utils";
import {
  RESETPWD,
  DEL,
  SEARCH,
  GETINFO,
  SETINFO,
  ADDTEACHER,
  ADDBYFILE,
} from "@/network/management";
export default {
  name: "",
  data() {
    //验证手机号
    var checkMobile = (rule, value, cb) => {
      const regMobile = /^[1](([3][0-9])|([4][0,1,4-9])|([5][0-3,5-9])|([6][2,5,6,7])|([7][0-8])|([8][0-9])|([9][0-3,5-9]))[0-9]{8}$/;

      if (regMobile.test(value)) {
        return cb();
      }
      cb(new Error("请输入合法手机号"));
    };
    //检验身份证
    var checkcardcode = (rule, value, callback) => {
      if (value) {
        if (!/(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/.test(value)) {
          callback(new Error("请输入正确的身份证号码"));
        } else {
          callback();
        }
      }
      callback();
    };
    //检验长度
    var checklen = (rule, value, callback) => {
      if (value) {
        if ((value + "").length !== 10) {
          callback(new Error("教职号长度必须为10个数字"));
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
      userlist: [],
      total: 0,
      DialogVisible: {
        delDialogVisible: false,
        resetDialogVisible: false,
        editinfoDialogVisible: false,
        adduserDialogVisible: false,
        allimportDialogVisible: false,
      },
      editInfoForm: {},
      addUserForm: {
        name: "",
        phonenum: "",
        cardno: "",
        TEID: "",
      },
      editFormRules: {
        phonenum: [
          { required: true, message: "请输入手机号", trigger: "blur" },
          { validator: checkMobile, trigger: "blur" },
        ],
        cardno: [
          { required: true, message: "请输入身份证号", trigger: "blur" },
          { validator: checkcardcode, trigger: "blur" },
        ],
        name: [
          { required: true, message: "请输入姓名", trigger: "blur" },
          {
            min: 2,
            max: 10,
            message: "名字长度在 2 到 10 个字",
            trigger: "blur",
          },
        ],
        TEID: [
          { required: true, message: "请输入教职号", trigger: "blur" },
          { type: "number", message: "教职号必须为数字值", trigger: "blur" },
          { validator: checklen, trigger: "blur" },
        ],
      },
      search: "",
      xlscList: [],
      xlscTitle: {
        教职号: "TEID",
        姓名: "name",
        身份证号: "cardno",
        联系方式: "phonenum",
      },
      xlsctotal: 0,
      datalist: [],
      clickusername: "",
      isrepeat: false,
      tablerule: {
        phonenum: /^0?(13|14|15|17|18|19)[0-9]{9}$/,
        TEID: /^[0-9]{10}$/,
        cardno: /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/,
      },
    };
  },
  created() {},
  mounted() {
    window.addEventListener("keydown", this.keyDown);
    this.search = debounce(this.searchInfo, 500, true);
    this.search();
  },
  methods: {
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
        "teacher",
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
    delteacher() {
      DEL(this.clickusername, "teacher").then((res) => {
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
      GETINFO(username, "teacher").then((res) => {
        this.editInfoForm = res.data.data;
        this.DialogVisible.editinfoDialogVisible = true;
      });
    },
    edituserinfo() {
      this.$refs.editFormRef.validate((valid) => {
        if (!valid) return;
        SETINFO(
          this.editInfoForm.TEID,
          this.editInfoForm.phonenum,
          "teacher"
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
    addteacher() {
      this.$refs.addFormRef.validate((valid) => {
        if (!valid) return;
        ADDTEACHER(
          this.addUserForm.TEID,
          this.addUserForm.name,
          this.addUserForm.phonenum,
          this.addUserForm.cardno,
          true
        ).then((res) => {
          let msg = res.data.status;
          if (msg == "has TEID") {
            this.$message.error("该教职号已存在");
          } else if (msg == "has signed") {
            this.$message.error("该身份证已被使用");
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
    addall() {
      this.DialogVisible.allimportDialogVisible = true;
    },
    addteacherbyfile() {
      if (this.isrepeat) return;
      let that = this;
      let flag = true;

      for (let [index, elem] of new Map(
        this.xlscList.map((item, i) => [i, item])
      )) {
        if (
          this.tablerule.TEID.test(elem.TEID) &&
          this.tablerule.phonenum.test(elem.phonenum) &&
          this.tablerule.cardno.test(elem.cardno) &&
          elem.name.length >= 2 &&
          elem.name.length <= 10
        ) {
          for (let item1 of that.datalist) {
            if (elem.TEID == item1.TEID) {
              flag = false;
              break;
            }
          }
          if (!flag) {
            this.$message.error("第" + (index + 1) + "条记录教职号已存在");
            break;
          }
          for (let item1 of that.datalist) {
            if (elem.cardno == item1.cardno) {
              flag = false;
              break;
            }
          }
          if (!flag) {
            this.$message.error("第" + (index + 1) + "条记录身份证号已被使用");
            break;
          }
        } else {
          flag = false;
          this.$message.error("第" + (index + 1) + "条记录为非法数据");
          break;
        }
      }
      if (flag) {
        ADDBYFILE(this.xlscList, "teacher", true).then((res) => {
          let msg = res.data.status;
           if (msg == "success") {
              this.$message({
                message: "批量添加成功",
                type: "success",
                duration: 2000,
              });
              this.DialogVisible.allimportDialogVisible = false;
              this.searchInfo(true, false);
            } else if (msg == "fail") {
              this.$message.error("添加失败");
            }
        });
      }
    },
    // 退出时清除表单内容
    editinfoDialogClosed() {
      this.$refs.editFormRef.resetFields();
    },
    adduserDialogClosed() {
      this.$refs.addFormRef.resetFields();
    },
    allimportDialogClosed() {
      this.xlsctotal = 0;
      this.xlscList = [];
      this.isrepeat = false;
    },
    //导入excel
    uploadChange(file) {
      this.xlsctotal = 0;
      this.xlscList = [];
      this.isrepeat = false;
      let self = this;
      const types = file.name.split(".")[1];
      const fileType = ["xlsx", "xlc", "xlm", "xls", "xlt", "xlw", "csv"].some(
        (item) => {
          return item === types;
        }
      );
      if (!fileType) {
        this.$message.error("文件格式错误，请重新选择文件！");
      }

      file2Xce(file).then((tab) => {
        // console.log(tab)
        // 过滤，转化正确的JSON对象格式
        if (tab && tab.length > 0) {
          tab[0].sheet.forEach((item) => {
            let obj = {};
            for (let key in item) {
              obj[self.xlscTitle[key]] = item[key];
            }
            self.xlscList.forEach((item) => {
              if (item.TEID === obj.TEID || item.cardno === obj.cardno) {
                this.isrepeat = true;
              }
            });
            self.xlscList.push(obj);
          });
          // console.log(self.xlscList)

          if (self.xlscList.length) {
            this.$message.success("导入成功");
            this.xlsctotal = self.xlscList.length; // 获取数据后，下一步操作
          } else {
            this.xlsctotal = 0;
            this.$message.error("空文件或数据缺失，请重新选择文件！");
          }
        }
      });
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