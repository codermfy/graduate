<!--  -->
<template>
  <div id="">
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home/experienments' }"
        >实验项目管理</el-breadcrumb-item
      >
      <el-breadcrumb-item>实验项目列表</el-breadcrumb-item>
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
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="search"
            ></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="additem">新增实验项目</el-button>
        </el-col>
      </el-row>
      <el-table :data="itemlist" border height="60vh">
        <el-table-column prop="itemid" label="实验ID" align="center" width='70px'>
        </el-table-column>
        <el-table-column prop="title" label="实验标题"> </el-table-column>
        <el-table-column label="操作" width="140px">
          <template v-slot="scope">
            <el-tooltip
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
                @click="del(scope.row.itemid)"
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
    <!-- 删除实验 -->
    <el-dialog
      title="删除实验项目"
      :visible.sync="DialogVisible.delDialogVisible"
      width="30%"
    >
      <span>是否确定<span class="deltip">删除</span>该项目?</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="DialogVisible.delDialogVisible = false"
          >取 消</el-button
        >
        <el-button
          type="primary"
          @click="delitem"
          >确 定</el-button
        >
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { debounce } from "@/common/utils";
import { DEL, SEARCH} from "@/network/management";
export default {
  name: "",
  data() {
    return {
         queryInfo: {
        query: "",
        pagenum: 1,
        querytype: "queryall",
        pagesize: 20,
      },
      itemlist:[

      ],
      total:0,
       DialogVisible: {
            delDialogVisible: false,
       },
       search:'',
      currentitemid: "",
      datalist: [],
    };
  },
  created() {},
  mounted() {
      window.addEventListener("keydown", this.keyDown);
    this.search = debounce(this.searchInfo, 500, true);
    this.search();
  },
  methods:{
     keyDown(e) {
      if (e.keyCode == 13 && this.$refs.searchInput.focused == true) {
        this.search();
      }
    }, 
     handleCurrentChange(val) {
      this.queryInfo.pagenum = val;
      this.itemlist = this.datalist.slice(
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
        "exdemo",
        loading
      ).then((res) => {
        this.datalist = res.data.data;
        this.total = this.datalist.length;
        this.itemlist = this.datalist.slice(
          this.queryInfo.pagesize * (this.queryInfo.pagenum - 1),
          this.queryInfo.pagesize * this.queryInfo.pagenum
        );
      });
    },

    del(username) {
      this.currentitemid=username;
      this.DialogVisible.delDialogVisible = true;
    },
    delitem(){
 DEL(this.currentitemid.toString(), "exdemo").then((res) => {
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
    editInfo(itemid) {
        window.sessionStorage.setItem("itemid", itemid);
        this.$router.push({ path: "/home/editexdemo" });
    },
    additem(){
         this.$router.push({ path: "/home/addexdemo" });
    }
  },
   destroyed() {
    window.removeEventListener("keydown", this.keyDown, false);
  },
};
</script>
<style lang='less' scoped>
</style>