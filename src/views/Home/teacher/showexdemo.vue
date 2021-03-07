<!--  -->
<template>
<div id="" class="editor">
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
        <el-page-header @back="goBack" :content="exdemo.title"> </el-page-header>
      </div>

            <div class="content">
            <h4>实验步骤：</h4>
      <el-divider></el-divider>
      <preview :edithtml="exdemo.steps" :files="exdemo.files"></preview>
      <div v-show="showvideo">
            <h4>实验演示：</h4>
      <el-divider></el-divider>
        <videoandupdate
        :videosrc="exdemo.videourl"
        :isshowupload="false"
        :isshowvideo="showvideo"
      ></videoandupdate>
      </div>
      </div>

</el-card>
</div>
</template>

<script>
import Preview from "../common/preview";
import Editarea from "../common/editarea";
import Videoandupdate from "../common/videoplayer";
import { GETEXDEMO } from "@/network/management";
export default {
    name:"",
    components: {
    Preview,
    Editarea,
    Videoandupdate,
  },
    data() {
        return {
  exdemo: {},
  itemid: "",
  showvideo:false
        }
    },
    created() {
    this.itemid = window.sessionStorage.getItem("itemid");

    },
    mounted() {
    this.getexdemo();
    },
    methods: {
    goBack() {
      window.sessionStorage.removeItem("itemid");
      this.$router.push({ path: "/home/experienmentdisplay" });
    },
    getexdemo() {
      GETEXDEMO(this.itemid).then((res) => {
        this.exdemo = res.data.data;
        // console.log(res.data.data)
        if(this.exdemo.videourl){
            this.showvideo=true
        }
      });
    },
  },
}
</script>
<style lang='less' scoped>
.content{
    width:65%;
    margin:0 auto;
}
</style>