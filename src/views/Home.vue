<!-- home页面 -->
<template>
  <div>
    <el-container class="home_container" v-if="!bshowmanagement">
      <el-header style="background: #545c64">
        <div class="top_logo">
          <!-- logo图片 -->
        </div>
        <div class="logout">
          <el-menu
            class="el-menu-demo"
            mode="horizontal"
            router
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#409EFF"
            style="width: 0%"
          >
            <el-submenu index="2">
              <template slot="title">
                <el-avatar
                  size="small"
                  src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"
                ></el-avatar>
                {{ name }}
              </template>
              <el-menu-item class="logout" @click="logout">退出</el-menu-item>
            </el-submenu>
          </el-menu>
        </div>
        <el-menu
          :default-active="$store.state.path"
          class="el-menu-demo"
          mode="horizontal"
          router
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#409EFF"
          @select="handleSelect"
        >
          <!-- <el-menu-item index="/home/first">首页</el-menu-item> -->
          <el-menu-item index="/home/projects">
            <el-badge :is-dot="isnew" class="item">实验项目</el-badge>
          </el-menu-item>

          <el-submenu index="2" v-if="bshowepm">
            <template slot="title">实验管理</template>
            <el-menu-item index="/home/experienmentdisplay"
              >实验项目演示</el-menu-item
            >
            <el-menu-item index="/home/experienmentfix">实验报修</el-menu-item>
          </el-submenu>
          <el-menu-item index="/home/statistics" v-if="bshowstatistic"
            >数据统计</el-menu-item
          >
          <el-menu-item index="/home/profile">个人信息</el-menu-item>
        </el-menu>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
      <!-- <el-footer height="30px">
        <p id="footer">&copy;2021-01-01&nbsp;MFY</p>
      </el-footer> -->
    </el-container>
    <el-container v-else class="home_management">
      <el-header class="header_management">
        <div>
          <img src="@/assets/img/logo.png" />
          <span>中学科学实验管理后台系统</span>
        </div>
        <div class="intro">
          <el-avatar icon="el-icon-user-solid"></el-avatar>
          <span>{{ name }}</span>
        </div>
        <el-button type="info" @click="logout">退出</el-button>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu
            class="el-menu-vertical-demo"
            :default-active="$store.state.path"
            @select="handleSelect"
            background-color="#333744"
            text-color="#fff"
            active-text-color="#409eff"
            router
          >
            <el-submenu index="1">
              <template slot="title">
                <i class="iconfont icon-users"></i>
                <span>用户管理</span>
              </template>
              <el-menu-item-group>
                <el-menu-item index="/home/admins"
                  ><i class="el-icon-menu"></i>管理员列表</el-menu-item
                >
                <el-menu-item index="/home/teachers"
                  ><i class="el-icon-menu"></i>教师列表</el-menu-item
                >
                <el-menu-item index="/home/students"
                  ><i class="el-icon-menu"></i>学生列表</el-menu-item
                >
              </el-menu-item-group>
            </el-submenu>
            <el-menu-item index="/home/classes">
              <i class="el-icon-s-grid"></i>
              <span slot="title">班级管理</span>
            </el-menu-item>
            <el-submenu index="3" class="exmanage">
              <template slot="title">
                <i class="el-icon-s-claim"></i>
                <!-- <span>实验管理</span> -->
                <el-badge :is-dot="hasfix">实验管理</el-badge>
              </template>
              <el-menu-item-group>
                <el-menu-item index="/home/experienments"
                  ><i class="el-icon-menu"></i>实验项目管理</el-menu-item
                >
                <el-menu-item index="/home/experienmentsfix"
                  ><i class="el-icon-menu"> </i
                  ><el-badge :is-dot="hasfix">实验物品报修</el-badge>
                </el-menu-item>
              </el-menu-item-group>
            </el-submenu>
          </el-menu>
        </el-aside>
        <el-main class="main_management">
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { HASNEWFIX } from "@/network/management";
export default {
  name: "",
  data() {
    return {
      isnew: false,
      bshowstatistic: true,
      bshowmanagement: false,
      bshowepm: true,
      hasfix: false,
      name: "",
      username: "",
      type: -1,
    };
  },
  created() {
    // this.activeIndex=window.sessionStorage.getItem('path')
    // console.log(this.$store.state.path);
    this.type = window.sessionStorage.getItem("type");
    this.name = window.sessionStorage.getItem("name");
    this.username = window.sessionStorage.getItem("username");
    this.userdefault(this.type, this.username);
  },
  mounted() {},
  methods: {
    handleSelect(key) {
      if (key === "/home/projects") {
        this.isnew = false;
      } else if (key === "/home/experienmentsfix") {
        this.hasfix = false;
      }
      // window.sessionStorage.setItem('path',key)
    },
    logout() {
      window.sessionStorage.clear();
      this.$router.push("/login");
    },
    userdefault(type, username) {
      if (type == 1) {
        this.bshowstatistic = false;
        this.bshowmanagement = false;
        this.bshowepm = false;
      } else if (type == 2) {
        this.bshowstatistic = true;
        this.bshowmanagement = false;
        this.bshowepm = true;
      } else if (type == 3) {
        this.bshowmanagement = true;
        this.hasfix=window.sessionStorage.getItem('hasfix')==="true"?true:false;
        
        if (this.$store.state.path === "/home/experienmentsfix") {
          this.hasfix = false;
        } else {
          // setTimeout(() => {
          //   this.HasNewFix();
          // }, 1300);
        }
      }
    },
    HasNewWork(username) {},
    // HasNewFix() {
    //   HASNEWFIX().then((res) => {
    //     this.hasfix = res.data.status;
    //   });
    // },
  },
};
</script>
<style lang='less' >
.home_container {
  height: 100%;
  position: relative;
}
.el-header {
  text-align: center;
  line-height: 60px;
  position: relative;
  .el-menu {
    width: 50%;
    margin: 0 auto;
  }
  .logout {
    width: 25%;
    position: absolute;
    display: flex;
    align-items: center;
    right: 0;
  }
}
.el-main {
  background: #f2f4f7;
  height: calc(100vh - 60px);
}
// .el-footer {
//   position: fixed;
//   bottom: 0;
//   left: 50%;
//   transform: translate(-50%, 0);
// }
#footer {
  font-size: 12px;
  color: #888;
}
.exmanage .el-badge {
  height: 30px;
  line-height: 30px;
}
// .logout {
//   float: right;
// }
.header_management {
  background-color: #373d41;
  display: flex;
  justify-content: space-between;
  padding-left: 10px;
  align-items: center;
  color: #fff;
  font-size: 20px;
  > div {
    display: flex;
    align-items: center;
    img {
      width: 40px;
      height: 40px;
    }
    span {
      margin-left: 15px;
    }
  }
  .intro {
    margin-left: auto;
    margin-right: 20px;
    span {
      margin-left: 0;
    }
  }
}
.el-aside {
  background: #333744;
  .el-menu {
    border: none;
  }
}
.home_management {
  height: 100vh;
}
.iconfont {
  margin-right: 10px;
}
.el-menu-item .el-badge__content {
  background: #ff0000;
  border: 0;
}
.el-submenu .el-badge__content {
  background: #ff0000;
  border: 0;
}
.el-submenu .el-badge__content.is-fixed.is-dot {
  right: 90px;
}
.el-submenu .el-menu-item .el-badge__content.is-fixed.is-dot {
  right: 120px;
}
.el-avatar {
  margin-right: 10px;
}
</style>