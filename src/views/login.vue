<!-- login页面 -->
<template>
  <div>
    <el-container>
      <el-header height="20vh"></el-header>
      <el-main>
        <div id="login_box">
          <div class="avatar_box">
            <img src="@/assets/img/logo.png" />
          </div>
          <el-form
            ref="form"
            :model="form"
            class="login_form"
            v-if="iloginformshow"
            :rules="rules"
          >
            <el-form-item prop="username">
              <el-input
                placeholder="请输入学号"
                prefix-icon="iconfont icon-user"
                maxlength="32"
                type="text"
                v-model="form.username"
              ></el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                placeholder="请输入密码"
                prefix-icon="iconfont icon-3702mima"
                maxlength="16"
                :type="inputtype"
                v-model="form.password"
              >
                <i
                  id="showedpwd"
                  slot="suffix"
                  class="el-icon-view"
                  v-show="ipwdshowed"
                  @click="showPwd"
                ></i>
                <i
                  slot="suffix"
                  class="el-icon-view"
                  v-show="ipwdshow"
                  @click="showPwd"
                ></i>
              </el-input>
            </el-form-item>
            <el-link type="info" @click="switchpage">忘记密码?</el-link>

            <el-form-item class="btn">
              <el-button type="primary" @click="login">登录</el-button>
            </el-form-item>
          </el-form>
          <!-- 忘记密码 -->
          <el-form
            ref="form"
            :model="form"
            class="forget_form"
            v-else
            :rules="rules"
          >
            <el-page-header @back="switchpage"> </el-page-header>
            <el-form-item prop="username">
              <el-input
                placeholder="请输入学号"
                prefix-icon="iconfont icon-user"
                maxlength="32"
                type="text"
                v-model="form.username"
              ></el-input>
            </el-form-item>
            <el-form-item prop="cardcode">
              <el-input
                placeholder="请输入身份证号"
                prefix-icon="iconfont icon-danju"
                maxlength="18"
                type="text"
                v-model="form.cardcode"
              >
              </el-input>
            </el-form-item>
            <el-form-item class="btn">
              <el-button type="success" @click="reset">重置密码</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-main>
      <el-footer height="20vh">
        <p id="footer">&copy;2021-01-01&nbsp;MFY</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import { Login, Reset } from "@/network/login.js";
import { HASNEWFIX } from "@/network/management";
import md5 from "js-md5";
export default {
  name: "login",
  data() {
    var checkcardcode = (rule, value, callback) => {
      if (value) {
        if (!/(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/.test(value)) {
          callback(new Error("请输入正确的身份证号码!"));
        } else {
          callback();
        }
      }
      callback();
    };
    var checkData = (rule, value, callback) => {
      if (value) {
        if (/[\u4E00-\u9FA5]/g.test(value)) {
          callback(new Error("不能输入汉字!"));
        } else {
          callback();
        }
      }
      callback();
    };
    return {
      form: {
        username: "",
        password: "",
        cardcode: "",
      },
      rules: {
        username: [
          { required: true, message: "请输入学号", trigger: "blur" },
          {
            min: 5,
            max: 32,
            message: "长度在 5 到 32 个字符",
            trigger: "blur",
          },
          { validator: checkData, trigger: "blur" },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          {
            min: 5,
            max: 16,
            message: "长度在 5 到 16 个字符",
            trigger: "blur",
          },
        ],
        cardcode: [
          { required: true, message: "请输入身份证号", trigger: "blur" },
          { validator: checkcardcode, trigger: "blur" },
        ],
      },
      ipwdshowed: false,
      ipwdshow: false,
      iloginformshow: true,
      inputtype: "password",
    };
  },
  created() {},
  mounted() {
    window.addEventListener("keydown", this.keyDown);
  },
  methods: {
    keyDown(e) {
      if (e.keyCode == 13) {
        this.iloginformshow ? this.login() : this.reset();
      }
    },
    login() {
      // this.$message({
      //       message: '登陆成功',
      //       type: 'success'
      //     });
      // this.$message.error('登陆失败，账号或密码错误!');
      this.$refs.form.validate((valid) => {
        if (!valid) return;
        Login(this.form.username, this.form.password)
          .then((res) => {
            var data = res.data[0];
            // console.log(md5(this.form.password))
            if (data.type == 0) {
              this.$message.error("登陆失败，账号或密码错误!");
            } else {
              // this.$store.commit('setusername',this.form.username)
              // this.$store.commit('settype',data.type)
              // this.$store.commit('setname',data.name)
              window.sessionStorage.setItem("username", this.form.username);
              window.sessionStorage.setItem("type", data.type);
              window.sessionStorage.setItem("name", data.name);
              window.sessionStorage.setItem("token", data.token);

              this.$message({
                message: "登陆成功",
                type: "success",
                duration: 1000,
              });
            }
            return data;
          })
          .then((data) => {
            HASNEWFIX().then((res) => {
              // this.hasfix = res.data.status;
              window.sessionStorage.setItem("hasfix", res.data.status);
              if (data.type == 3) {
                this.$router.push({ path: "/home/admins" });
              } else {
                this.$router.push({ path: "/home/projects" });
              }
            });
          });
      });
    },
    reset() {
      this.$refs.form.validate((valid) => {
        if (!valid) return;
        Reset(this.form.username, this.form.cardcode).then((res) => {
          var data = res.data[0];
          if (data.message == "fail") {
            this.$message.error("重置失败,未知错误");
          } else if (data.message == "wrong") {
            this.$message.error("重置失败,账号或身份证错误");
          } else {
            this.$message({
              message: "重置成功,密码为身份证后6位",
              type: "success",
            });
          }
        });
      });
    },
    showPwd() {
      this.ipwdshow = !this.ipwdshow;
      this.ipwdshowed = !this.ipwdshowed;
      this.inputtype = this.ipwdshowed ? "text" : "password";
      let e = document.getElementsByClassName("el-icon-view")[0];
      this.ipwdshowed
        ? e.setAttribute("style", "color: #000000")
        : e.setAttribute("style", "color: #c0c4cc");
    },
    switchpage() {
      this.iloginformshow = !this.iloginformshow;
      this.$refs.form.resetFields();
    },
  },
  watch: {
    "form.password": {
      handler(newval, oldval) {
        if (newval !== "") {
          this.ipwdshow = true;
        } else {
          this.ipwdshowed = false;
          this.ipwdshow = false;
        }
      },
      immediate: true,
    },
  },
  destroyed() {
    window.removeEventListener("keydown", this.keyDown, false);
  },
};
</script>
<style lang='less' scoped>
.el-header,
.el-footer {
  display: flex;
  justify-content: center;
  align-items: center;
}
.el-main {
  height: 60vh;
  background: url(../assets/img/login_background.jpg) center center no-repeat;
  background-size: 100% 100%;
  position: relative;
}
#footer {
  font-size: 12px;
  color: #888;
}
#login_box {
  height: 40vh;
  width: 60vh;
  position: absolute;
  left: 60%;
  top: 50%;
  transform: translate(0, -50%);
  background: #fff;
  border-radius: 3px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}
.avatar_box {
  height: 15vh;
  width: 15vh;
  border: 1px solid #eee;
  border-radius: 50%;
  box-shadow: 0 0 3px;
  position: absolute;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff;
  img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background-color: #eee;
  }
}
.login_form,
.forget_form {
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 0 20px;
  box-sizing: border-box;
}
.el-link {
  font-size: 12px;
  position: absolute;
  top: 65%;
}
.btn {
  display: flex;
  justify-content: flex-end;
}
.el-page-header {
  position: absolute;
  top: -40px;
  left: 20px;
}
</style>