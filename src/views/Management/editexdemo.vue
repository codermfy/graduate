<!--  -->
<template>
  <div id="" class="editor">
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home/experienments' }"
        >实验项目管理</el-breadcrumb-item
      >
      <el-breadcrumb-item>实验项目列表</el-breadcrumb-item>
      <el-breadcrumb-item>编辑实验项目</el-breadcrumb-item>
    </el-breadcrumb>
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
        <el-page-header @back="goBack" content="编辑演示项目"> </el-page-header>
        <div>
          <span v-if="true">
            <el-button type="success" @click="save">保存修改</el-button>
          </span>
        </div>
      </div>
      <el-form
        :model="exdemo"
        :rules="editrules"
        ref="ruleForm"
        label-width="85px"
      >
        <el-form-item label="实验标题" prop="title">
          <el-col :span="10">
            <el-input
              v-model="exdemo.title"
              placeholder="请输入实验标题"
            ></el-input>
          </el-col>
        </el-form-item>
      </el-form>
      <h4>预览：</h4>
      <el-divider></el-divider>
      <preview :edithtml="tempsteps" :files="exdemo.files"></preview>
      <h4>实验步骤：</h4>
      <el-divider></el-divider>
      <editarea
        :edithtml="exdemo.steps"
        :isshow="true"
        :files="exdemo.files"
        @changetxt="updatetxt"
        @changefilelist="updatefiles"
      ></editarea>
      <h4>视频上传：</h4>
      <el-divider></el-divider>
      <videoandupdate
        :videosrc="exdemo.videourl"
        :isshowupload="true"
        :isshowvideo="true"
        @changevideosrc="updatesrc"
      ></videoandupdate>
    </el-card>
  </div>
</template>

<script>
import Preview from "../Home/common/preview";
import Editarea from "../Home/common/editarea";
import Videoandupdate from "../Home/common/videoplayer";
import { GETEXDEMO, EDITEXDEMO } from "@/network/management";

export default {
  name: "",
  components: {
    Preview,
    Editarea,
    Videoandupdate,
  },
  data() {
    return {
      exdemo: {},
      editrules: {
        title: [{ required: true, message: "请输入标题", trigger: "blur" }],
      },
      tempsteps: "",
      itemid: "",
    };
  },
  created() {
    this.itemid = window.sessionStorage.getItem("itemid");
  },
  mounted() {
    this.tempsteps = this.exdemo.steps;
    this.getexdemo();
  },
  methods: {
    goBack() {
      window.sessionStorage.removeItem("itemid");
      this.$router.push({ path: "/home/experienments" });
    },
    getexdemo() {
      GETEXDEMO(this.itemid).then((res) => {
        this.exdemo = res.data.data;
        // console.log(res.data.data)
      });
    },
    save() {
      this.exdemo.steps = this.tempsteps;
      this.$refs.ruleForm.validate((valid) => {
        if (!valid) return;
        EDITEXDEMO(this.exdemo, true).then((res) => {
          let status = res.data.status;
          if (status == "success") {
            this.$message({
              message: "修改成功",
              type: "success",
              duration: 2000,
            });
          } else {
            this.$message.error("修改失败");
          }
        });
      });
    },
    updatetxt(html) {
      this.tempsteps = html;
    },
    updatefiles(file) {
      this.exdemo.files.unshift(file);
    },
    updatesrc(src) {
      this.exdemo.videourl = src;
    },
  },
};
</script>
<style lang='less' scoped>
</style>