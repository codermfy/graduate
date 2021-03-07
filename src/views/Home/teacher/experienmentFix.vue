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
        <div class="radio">
          <span style="color: #606266">筛选：</span>
          <el-radio-group v-model="querytype">
            <el-radio label="TEID">全部</el-radio>
            <el-radio label="waitdone">待处理</el-radio>
            <el-radio label="isdone">已处理</el-radio>
            <el-radio label="dontdone">已退回</el-radio>
          </el-radio-group>
        </div>
        <el-button type="primary" @click="adddialogopen">物品报修</el-button>
      </div>

      <el-table :data="goodlist" border>
        <el-table-column
          prop="fixid"
          label="报修单号"
          align="center"
          width="100px"
        >
        </el-table-column>
        <el-table-column
          prop="goodsname"
          label="物品名称"
          width="200px"
        ></el-table-column>
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
        <el-table-column prop="state" label="状态" width="100px" align="center">
          <template v-slot="scope">
            <el-tag
              type="success"
              v-if="scope.row.isdone == 1 && scope.row.isused == 1"
              >已处理</el-tag
            >
            <el-tag
              type="warning"
              v-if="scope.row.isdone == 0 && scope.row.isused == 1"
              >待处理</el-tag
            >
            <el-tag
              type="danger"
              v-if="scope.row.isdone == 0 && scope.row.isused == 0"
              >已退回</el-tag
            >
          </template>
        </el-table-column>
        <el-table-column label="操作" width="90px">
          <template v-slot="scope">
            <el-tooltip
              v-if="scope.row.isdone != 1"
              effect="dark"
              content="删除"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="danger"
                icon="el-icon-delete"
                size="mini"
                @click="deldialogopen(scope.row.fixid)"
              ></el-button>
            </el-tooltip>
            <div v-if="scope.row.isdone != 0">
              <el-tag type="">{{ "费用:" + scope.row.cost }}</el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="charge" label="处理人" width="180px">
        </el-table-column>
      </el-table>
    </el-card>
    <el-dialog
      title="删除记录"
      :visible.sync="DialogVisible.delDialogVisible"
      width="30%"
    >
      <span>是否确定<span class="deltip">删除</span>该条记录?</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible.delDialogVisible = false"
          >取 消</el-button
        >
        <el-button type="primary" @click="delfixrecord">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="物品保修"
      :visible.sync="DialogVisible.addDialogVisible"
      width="30%"
      @close="adddialogclose"
    >
      <el-form
        :model="fixrecord"
        :rules="rules"
        ref="ruleForm"
        label-width="100px"
      >
        <el-form-item label="物品类型" prop="goodstype">
          <el-select v-model="fixrecord.goodstype">
            <el-option label="实验仪器" value="1"></el-option>
            <el-option label="化学药品" value="2"></el-option>
            <el-option label="其他" value="3"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="物品名称" prop="goodsname" v-if="showgoods">
          <el-select v-model="fixrecord.goodsname">
            <el-option
              v-for="item in currentlist"
              :key="item"
              :label="item"
              :value="item"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="物品名称" prop="goodsname" v-if="!showgoods">
          <el-input v-model="fixrecord.goodsname"></el-input>
        </el-form-item>
        <el-form-item label="数量">
          <el-input-number
            v-model="fixrecord.goodsnum"
            :min="1"
            :max="10"
          ></el-input-number>
        </el-form-item>
        <el-form-item label="情况描述" prop="goodsdesc">
          <el-input type="textarea" v-model="fixrecord.goodsdesc"  maxlength="50" autosize></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible.addDialogVisible = false"
          >取 消</el-button
        >
        <el-button type="primary" @click="addfixrecord">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { SEARCH } from "@/network/management";
import { DELFIX, ADDFIX } from "@/network/teacher";
export default {
  name: "",
  data() {
    return {
      querytype: "TEID",
      username: "",
      goodlist: [],
      clickfixid: "",
      showgoods: true,
      DialogVisible: {
        delDialogVisible: false,
        addDialogVisible: false,
      },
      fixrecord: {
        goodsname: "",
        goodstype: "",
        goodsnum: 1,
        goodsdesc: "",
      },
      rules: {
        goodstype: [
          { required: true, message: "请选择物品类型", trigger: "change" },
        ],
        goodsdesc: [
          { required: true, message: "请填写情况描述", trigger: "blur" },
        ],
        goodsname: [
          {
            required: true,
            message: "请添加物品名称",
            trigger: ["blur", "change"],
          },
        ],
      },
      goodsnamelist: {
        1: [
          "试管",
          "烧杯",
          "蒸发皿",
          "坩埚",
          "酒精灯",
          "布氏漏斗",
          "洗气瓶",
          "干燥管",
          "托盘天平",
          "量筒",
          "容量瓶",
          "滴定管",
          "量器",
        ],
        2: [
          "盐酸",
          "硫酸",
          "硝酸",
          "氢氧化钠",
          "氢氧化钙",
          "氨水",
          "氯化钠",
          "碳酸钠",
          "硫酸铜",
          "氯化铁",
          "氯化亚铁",
        ],
      },
      currentlist: [],
    };
  },
  created() {
    this.username = window.sessionStorage.getItem("username");
  },
  mounted() {
    this.search();
  },
  methods: {
    search() {
      SEARCH(this.username, this.querytype, "exgood").then((res) => {
        this.goodlist = res.data.data;
      });
    },
    deldialogopen(fixid) {
      this.clickfixid = fixid;
      this.DialogVisible.delDialogVisible = true;
    },
    delfixrecord() {
      DELFIX(this.clickfixid).then((res) => {
        let msg = res.data.status;
        if (msg == "success") {
          this.$message({
            message: "删除成功",
            type: "success",
            duration: 2000,
          });
          this.DialogVisible.delDialogVisible = false;
          this.search();
        } else if (msg == "fail") {
          this.$message.error("删除失败");
        }
      });
    },
    adddialogopen() {
      this.DialogVisible.addDialogVisible = true;
    },
    addfixrecord() {

      this.$refs.ruleForm.validate((valid) => {
        if (!valid) return;
        ADDFIX(this.fixrecord, this.username, true).then((res) => {
          let msg = res.data.status;
          if (msg == "success") {
            this.$message({
              message: "添加成功",
              type: "success",
              duration: 2000,
            });
            this.DialogVisible.addDialogVisible = false;
            this.search();
          } else {
            this.$message.error("添加失败");
          }
        });
      });
    },
    adddialogclose() {
      this.$refs.ruleForm.resetFields();
      this.fixrecord.goodsnum=1;
    },
  },
  watch: {
    querytype(val) {
      this.search();
    },
    "fixrecord.goodstype": function (val) {
      if (val == "3") {
        this.showgoods = false;
        this.fixrecord.goodsname = "";
      } else {
        this.showgoods = true;
        this.fixrecord.goodsname = "";
        this.currentlist = this.goodsnamelist[val];
      }
    },
  },
};
</script>
<style lang='less' scoped>
</style>