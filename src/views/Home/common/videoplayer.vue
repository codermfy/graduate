<!--  -->
<template>
  <div id="" >
    <el-upload
    v-if="isshowupload"
      　　　　action="/api/upload-video"
      　　　　:show-file-list="false"
      　　:on-success="handlesuccess"
      :on-error="handleerror"
      :headers="headerinfo"
      　　　　:auto-upload="true"
      accept=".mp4"
      :before-upload="beforeUpload"
      style="margin-left: auto; margin-bottom: 20px"
    >
      <el-button size="small" icon="el-icon-upload" type="primary"
        >上传视频</el-button
      >
    </el-upload>
    <div  v-show="isshowvideo">
    <video-player
      class="video-player vjs-custom-skin"
      style="width: 50%"
      ref="videoPlayer"
      :playsinline="true"
      :options="playerOptions"
    >
    </video-player>
    </div>
  </div>
</template>

<script>
import { videoPlayer } from "vue-video-player";
import "video.js/dist/video-js.css";
export default {
  name: "",
  components: {
    videoPlayer,
  },
  props:{
      videosrc:{
          type:String,
          require:true,
          default:''
      },
      isshowupload:{
          type:Boolean,
          default:false,
      },
      isshowvideo:{
          type:Boolean,
          default:false,
      }

  },
  data() {
    return {
      playerOptions: {
        playbackRates: [0.5, 1.0, 1.5, 2.0], // 可选的播放速度
        autoplay: false, // 如果为true,浏览器准备好时开始回放。
        muted: false, // 默认情况下将会消除任何音频。
        loop: false, // 是否视频一结束就重新开始。
        preload: "auto", // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
        language: "zh-CN",
        aspectRatio: "16:9", // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
        fluid: true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
        sources: [
          {
            type: "video/mp4", // 类型
            src: "", // url地址
          },
        ],
        poster: "", // 封面地址
        notSupportedMessage: "未上传视频文件", // 允许覆盖Video.js无法播放媒体源时显示的默认信息。
        controlBar: {
          timeDivider: true, // 当前时间和持续时间的分隔符
          durationDisplay: true, // 显示持续时间
          remainingTimeDisplay: false, // 是否显示剩余时间功能
          fullscreenToggle: true, // 是否显示全屏按钮
        },
      },
      headerinfo: {},
    };
  },
  created() {
    this.headerinfo = {
      Authorzation: window.sessionStorage.getItem("token"), // 设置请求头
    };
  },
  mounted() {
    // this.$refs.videoPlayer.player.play() // 播放
    // this.$refs.videoPlayer.player.pause() // 暂停
    // this.$refs.videoPlayer.player.src(src) // 重置进度条
  },
  methods: {
    handlesuccess(response, file, fileList) {
      //   let thefile=response.data[0]
        this.$emit("changevideosrc", response.data[0].url);
      this.$message({
          message: "上传成功!",
          type: "success",
        });
    // this.playerOptions.sources[0].src=response.data[0].url
    // console.log(file)
    },
    handleerror(err, file, fileList) {
      console.log("error", err);
      this.$message({
          message: "上传失败!",
          type: "danger",
        });
    },
    beforeUpload(file) {
      var testmsg = file.name.substring(file.name.lastIndexOf(".") + 1);
      const extension = testmsg === "mp4";
      if (!extension) {
        this.$message({
          message: "上传文件只能是mp4格式!",
          type: "warning",
        });
      }
      return extension;
    },
  },
  watch:{
      videosrc(val){
          this.playerOptions.sources[0].src=val
      }
  }
};
</script>
<style lang='less' scoped>
</style>