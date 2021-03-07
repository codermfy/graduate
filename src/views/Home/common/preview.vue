<!--  -->
<template>
  <div id="">
    <div v-if="!reverse" class='previewarea'>
      <div v-html="edithtml"></div>
      <div class="file" v-if="files.length != 0">
        <div class="fileitem" v-for="(i, index) in files" :key="index">
          <label @click="download(i.name, i.url)" :data-title="i.name"
            ><i class="el-icon-document"></i><span>{{ i.name }}</span></label
          >
        </div>
      </div>
    </div>
    <div v-else class='previewarea'>
      <div class="file" v-if="files.length != 0">
        <div class="fileitem" v-for="(i, index) in files" :key="index">
          <label @click="download(i.name, i.url)" :data-title="i.name"
            ><i class="el-icon-document"></i><span>{{ i.name }}</span></label
          >
        </div>
      </div>
      <div v-html="edithtml"></div>
    </div>
  </div>
</template>

<script>
import fileDownload from "js-file-download";
import axios from "axios";
export default {
  name: "preview",
  props: {
    edithtml: {
      type: String,
      require: true,
    },
    reverse: {
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
    return {};
  },
  created() {},
  mounted() {},
  methods: {
    download(name, url) {
      axios
        .get("/file" + url, {
          responseType: "blob", //返回的数据类型
        })
        .then((res) => {
          fileDownload(res.data, name);
        });
    },
  },
};
</script>
<style lang='less' scoped>
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
    white-space: nowrap;
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
.previewarea {
  min-height: 100px;
}
</style>