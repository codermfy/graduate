<!--  -->
<template>
  <div id="">
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home/experienmentsfix' }"
        >报修物品管理</el-breadcrumb-item
      >
      <el-breadcrumb-item>报修物品列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-row :gutter="20">
        <el-col :span="10">
          <el-input
            placeholder="请输入报修单号"
            class="input-with-select"
            ref="searchInput"
            v-model="queryInfo.query"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="search"
            ></el-button>
          </el-input>
        </el-col>
      </el-row>
      <el-table :data="goodslist" border height="60vh">
        <el-table-column
          prop="fixid"
          label="报修单号"
          align="center"
          width="100px"
        >
        </el-table-column>
        <el-table-column prop="goodsname" label="物品名称" width="200px">
        </el-table-column>
        <el-table-column
          prop="goodstype"
          label="物品类型"
          width="80px"
          align="center"
        >
        </el-table-column>
        <el-table-column
          prop="goodsnum"
          label="数量"
          width="50px"
          align="center"
        >
        </el-table-column>
        <el-table-column prop="goodsdesc" label="描述"> </el-table-column>
        <el-table-column prop="teacher" label="申请人" width="180px">
        </el-table-column>
        <el-table-column prop="state" label="状态" width="100px" align="center">
          <template v-slot="scope">
            <el-tag type="success" v-if="scope.row.isdone == 1">已完成</el-tag>
            <el-tag type="warning" v-if="scope.row.isdone == 0">待处理</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="140px">
          <template v-slot="scope">
            <!-- <el-tooltip
              effect="dark"
              content="详细信息"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="primary"
                icon="el-icon-document"
                size="mini"
                @click="editInfo(scope.row.itemid)"
              ></el-button>
            </el-tooltip> -->

            <el-tooltip
              v-if="scope.row.isdone == 0"
              effect="dark"
              content="完成"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="success"
                icon="el-icon-check"
                size="mini"
                @click="complete(scope.row.fixid)"
              ></el-button>
            </el-tooltip>

            <el-tooltip
              v-if="scope.row.isdone == 0"
              effect="dark"
              content="不处理"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="danger"
                icon="el-icon-close"
                size="mini"
                @click="del(scope.row.fixid)"
              ></el-button>      
            </el-tooltip>
            <div v-if="scope.row.isdone != 0">
            <el-tag type=""  >{{"费用:"+scope.row.cost}}</el-tag>
            </div>
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
    <!-- 不处理保修单 -->
    <el-dialog
      title="提示"
      :visible.sync="DialogVisible.delDialogVisible"
      width="30%"
    >
      <span>是否确定<span class="deltip">不处理</span>该项目?</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible.delDialogVisible = false"
          >取 消</el-button
        >
        <el-button
          type="primary"
          @click="delgood"
          >确 定</el-button
        >
      </span>
    </el-dialog>
    <!-- 详细信息 -->
    <!-- 完成 -->
    <el-dialog
      title="提示"
      :visible.sync="DialogVisible.completeDialogVisible"
      width="30%"
      @close="completeDialogClosed"
    >
       <el-form
        :model="finishForm"
        :rules="FormRules"
        ref="finishFormRef"
        label-width="90px"
      >

        <el-form-item label="报修费用" prop="cost">
          <el-input v-model.number="finishForm.cost">
            <template slot="append">元</template>
          </el-input>
          
        </el-form-item>

      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible.completeDialogVisible = false"
          >取 消</el-button
        >
        <el-button
          type="primary"
          @click="finished"
          >确 定</el-button
        >
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { debounce } from "@/common/utils";
import { DEL, SEARCH,HASFINISHED } from "@/network/management";

export default {
  name: "",
  data() {
    var checkval = (rule, value, callback) => {
      if (value < 0) {
        callback(new Error("费用不能为负数"));
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
      goodslist: [
      
      ],
      total: 0,
      DialogVisible: {
        delDialogVisible: false,
        // editinfoDialogVisible: false,
        completeDialogVisible: false,
      },
      finishForm: {
        cost:0,
      },
      FormRules: {
        cost: [
          { required: true, message: "请输入费用", trigger: "blur" },
          { type: "number", message: "费用必须为数字值", trigger: "blur" },
          { validator: checkval, trigger: "blur" },
        ],
      },
       search: "",
       clickusername: "",
      datalist: [],
      currentuser:""
    };
  },
  created() {
    this.currentuser = window.sessionStorage.getItem("username");
  },
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
      this.goodslist = this.datalist.slice(
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
        "exgood",
        loading
      ).then((res) => {
        this.datalist = res.data.data;
        this.total = this.datalist.length;
        this.goodslist = this.datalist.slice(
          this.queryInfo.pagesize * (this.queryInfo.pagenum - 1),
          this.queryInfo.pagesize * this.queryInfo.pagenum
        );
      });
    },
    del(username) {
      this.clickusername = username;
      this.DialogVisible.delDialogVisible = true;
    },
     delgood() {
      DEL(this.clickusername.toString(), "exgood").then((res) => {
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
    // editInfo(username) {
    //   this.DialogVisible.editinfoDialogVisible = true;
    // },
    complete(username) {
       this.clickusername = username;
      this.DialogVisible.completeDialogVisible = true;
    },
    finished(){
      HASFINISHED(this.clickusername.toString(),this.finishForm.cost.toString(),this.currentuser,true).then(res=>{
        let msg = res.data.status;
        if (msg == "success") {
            this.$message({
              message: "报修完成",
              type: "success",
              duration: 2000,
            });
            this.DialogVisible.completeDialogVisible = false;
            this.searchInfo(true, false);
          } else if (msg == "fail") {
            this.$message.error("提交失败");
          }
      })
    },
    completeDialogClosed(){
      this.$refs.finishFormRef.resetFields();
    }
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