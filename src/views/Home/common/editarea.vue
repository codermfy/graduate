<!--  -->
<template>
  <div id="">
    <div v-if="isshow">
      <div id="report_tool"></div>
      <div class="file">
        <div>
          <div class="fileitem" v-for="(i, index) in files" :key="index">
            <label @click="download(i.name,i.url)" :data-title="i.name"
              ><i class="el-icon-document"></i><span>{{i.name}}</span></label
            >
            <el-button v-if="true" type="text" @click="deletefile(index,i.name)"
              ><i class="el-icon-close"></i
            ></el-button>
          </div>
        </div>
        <el-upload
          　　　　action="/api/upload-file"
          　　　　:show-file-list="false"
          　　:on-success="handlesuccess"
              :on-error="handleerror"
          multiple
          :headers="headerinfo"
          　　　　:auto-upload="true"
          style="margin-left: auto"
        >
          <el-button size="small" icon="el-icon-upload" type="primary"
            >上传文件</el-button
          >
        </el-upload>
      </div>
      <div id="report_text"></div>
    </div>
  </div>
</template>

<script>
import E from "wangeditor";
import fileDownload from 'js-file-download'
import axios from 'axios'
export default {
  name: "",
  props: {
    edithtml: {
      type: String,
      require: true,

    },
    isshow: {
      type: Boolean,
      default: false,
    },
    files: {
      type: Array,
      default() {
        return [];
      },
    },
  },
  data() {
    return {
      editor: null,
      filelist: [],
      headerinfo: {},
    };
  },
  created() {
    this.headerinfo = {
      Authorzation: window.sessionStorage.getItem("token"), // 设置请求头
    };
  },
  mounted() {
    if (this.isshow) {
      this.editorinit();
    }
  },
  methods: {
    editorinit() {
      var that = this;
      this.editor = new E("#report_tool", "#report_text");
      this.editor.config.placeholder = "请输入内容";
      this.editor.config.excludeMenus = ["code", "video"];
      // 配置alt选项
      this.editor.config.showLinkImgAlt = false;
      // 配置超链接
      this.editor.config.showLinkImgHref = false;
      this.editor.config.uploadFileName = "file"; // formdata中的name属性
      this.editor.config.debug = true; // 开启debug模式
      this.editor.config.uploadImgServer = "/api/upload-img";
      // this.editor.config.withCredentials = true;
      this.editor.config.uploadImgHeaders = {
        Authorzation: window.sessionStorage.getItem("token"), // 设置请求头
      };
      this.editor.config.uploadImgHooks = {
        fail: function (xhr, editor, resData) {
          console.log("fail", resData);
        },
        // 上传图片出错，一般为 http 请求的错误
        error: function (xhr, editor, resData) {
          console.log("error", xhr, resData);
        },
        // 上传图片超时
        timeout: function (xhr) {
          console.log("timeout");
        },
        customInsert: function (insertImgFn, result) {
          // result 即服务端返回的接口
          

          // insertImgFn 可把图片插入到编辑器，传入图片 src ，执行函数即可
          result.data.forEach((element) => {
            insertImgFn(element.url);
          });
        },
      };
      this.editor.config.onchange = function (html) {
        that.$emit("changetxt", html);
      };
      // this.editor.config.onchangeTimeout = 1000;
      this.editor.create();
      
    },
    download(name,url) {
      axios.get('/file'+url, {
        responseType: 'blob' //返回的数据类型
    })
    .then(res => {
        fileDownload(res.data, name)
    })     
    },
    deletefile(index,filename){
      this.$confirm(`确定移除 ${ filename }？`).then(()=>{
        this.files.splice(index,1)
      }).catch(()=>{

      })
      
    },
    handlesuccess(response, file, fileList){
      let thefile=response.data[0]
      this.$emit("changefilelist", thefile);
    },
    handleerror(err, file, fileList){
       console.log("error", err);
    }
  },
  watch:{
    edithtml(){
      if(this.isshow){
      this.editor.txt.html(this.edithtml);
      }
    }
  }
};
</script>
<style lang='less' scoped>
// @import url("../../../assets/css/editorcss.css");
#report_tool {
  border: 1px solid #ccc;
}
#report_text {
  border: 1px solid #ccc;
  min-height: 300px;
}
.file {
  min-height: 60px;
  display: flex;
  align-items: center;
}
.fileitem {
  display: inline-block;
  padding: 10px 0px;
  margin: 5px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3), 0 0 6px rgba(0, 0, 0, 0.3);
  label {
    display: inline-block;
    margin-right: 10px;
    padding: 0 0 0 5px;
    cursor: pointer;
    color: #606266;
    position: relative;
  }
  span {
    display: inline-block;
    width: 100px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space:nowrap; 
    vertical-align: middle;
  }
  label:hover span {
    color: #409eff;
  }
  label:hover::after{
    content: attr(data-title);
    display: inline-block;
    position: absolute;
    white-space:nowrap; 
    top:-30px;
    left:20px;
    padding: 5px 7px;
    border: 1px solid #ddd;
    background:#eeeeee;
    border-radius: 5px;
    z-index: 2005;
  }
  i {
    vertical-align: middle;
    padding: 0px 8px;
  }
  .el-button {
    color: #000;
    float: right;
    padding: 2px 0px;
    font-size: 10px;
  }
  .el-button:hover {
    color: #409eff;
  }
}
</style>