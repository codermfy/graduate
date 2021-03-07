<!--  -->
<template>
  <div id="project">
    <el-container>
      <el-aside width="200px">
        <el-menu
          :default-active="activeIndex"
          class="el-menu-vertical-demo"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#409EFF"
          @select="selecthandle"
        >
          <el-menu-item index="1">
            <i class="el-icon-document"></i>
            <span slot="title">班级数据</span>
          </el-menu-item>
          <el-menu-item index="2">
            <i class="el-icon-document"></i>
            <span slot="title">学生数据</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <div class="head">
          <div class="radio">
            <span style="color: #606266">筛选：</span>
            <el-radio-group v-model="querytype">
              <el-radio label="all" v-show="activeIndex == '2'">全部</el-radio>
              <el-radio
                v-for="(classno, index) in classnolist"
                v-bind:key="index"
                :label="classno"
              >
                {{ classno }}
              </el-radio>
            </el-radio-group>
          </div>
          <el-radio-group
            v-model="isCollapse"
            v-show="activeIndex == '1'"
            class="switchbtn"
          >
            <el-radio-button :label="true"
              ><i class="el-icon-menu"></i
            ></el-radio-button>
            <el-radio-button :label="false"
              ><i class="el-icon-s-data"></i
            ></el-radio-button>
          </el-radio-group>
          <el-divider></el-divider>
        </div>
        <el-row
          class="el-row statistics"
          :gutter="30"
          v-show="queryrole == 'class' && isCollapse == true"
        >
          <el-col
            v-for="(item, index) in projectlist"
            v-bind:key="index"
            :span="6"
          >
            <el-card shadow="hover" class="project">
              <div
                slot="header"
                class="clearfix"
                @click="projectinfo(item.EXPID)"
              >
                <el-badge class="title">{{ item.title }}</el-badge>
              </div>
              <div class="item">
                {{ "平均分数：" + item.averagegrade }}
              </div>
              <div class="item">
                {{ "提交率：" + item.submitlv + "%" }}
              </div>
              <el-button
                style="float: right"
                type="info"
                size="mini"
                icon="el-icon-s-order"
                @click="projectinfo(item.EXPID)"
                >查看详情</el-button
              >
            </el-card>
          </el-col>
        </el-row>
        <div v-show="queryrole == 'class' && isCollapse == false">
          <div id="main" style="width: 1000px; height: 500px"></div>
        </div>
        <div v-show="queryrole == 'student'">
          <el-table
            :data="
              studentlist.filter(
                (data) =>
                  !search ||
                  data.name.toLowerCase().includes(search.toLowerCase())
              )
            "
            border
          >
            <el-table-column type="index" align="center"></el-table-column>
            <el-table-column prop="STID" label="学号"> </el-table-column>
            <el-table-column prop="name" label="姓名"></el-table-column>
            <el-table-column prop="classno" label="班级"></el-table-column>
            <el-table-column
              prop="averagegrade"
              label="平均成绩"
              sortable
            ></el-table-column>
            <el-table-column prop="submitlv" label="作业提交率" sortable>
            </el-table-column>
            <el-table-column>
              <template slot="header" slot-scope="scope">
                <el-input
                  v-model="search"
                  size="mini"
                  placeholder="输入姓名搜索"
                />
              </template>
              <template slot-scope="scope">
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
                    @click="getInfo(scope.row.STID)"
                  ></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-main>
    </el-container>
    <el-dialog
      title="成绩列表"
      :visible.sync="projectdialogVisible"
      width="80%"
    >
      <el-table :data="projectrecord" border>
        <el-table-column type="index" align="center"></el-table-column>
        <el-table-column prop="STID" label="学号"> </el-table-column>
        <el-table-column prop="name" label="姓名"></el-table-column>
        <el-table-column label="状态" width="70px">
          <template v-slot="scope">
            <p v-if="scope.row.status == '0'" style="color: red">未完成</p>
            <p v-else-if="scope.row.status == '1'">待批阅</p>
            <p v-else-if="scope.row.status == '2'" style="color: green">
              已完成
            </p>
          </template>
        </el-table-column>
        <el-table-column
          prop="subtime"
          label="提交时间"
          sortable
        ></el-table-column>
        <el-table-column prop="grade" label="成绩" sortable width="80px">
        </el-table-column>
      </el-table>
    </el-dialog>
    <el-dialog title="成绩统计" :visible.sync="recorddialogVisible" width="70%">
      <div id="everyrecord" style="width: 70%; height: 500px"></div>
    </el-dialog>
  </div>
</template>

<script>
import * as echarts from "echarts";
import {
  GETCLASSLIST,
  GETSTATISTICS,
  SEARCHSUBMITLIST,
  GETALLRECORDS,
} from "@/network/teacher";

export default {
  name: "",
  data() {
    return {
      activeIndex: "1",
      querytype: "all",
      username: "",
      classnolist: [],
      queryrole: "class",
      isCollapse: true,
      projectlist: [],
      projectrecord: [],
      projectdialogVisible: false,
      studentlist: [],
      search: "",
      recorddialogVisible: false,
    };
  },
  created() {
    this.username = window.sessionStorage.getItem("username");
  },
  mounted() {
    this.getclass();
  },
  methods: {
    getclass() {
      GETCLASSLIST(this.username).then((res) => {
        this.classnolist = res.data.data;
        if (this.activeIndex == "1") {
          this.querytype = this.classnolist[0];
          this.queryrole = "class";
        } else {
          this.querytype = "all";
          this.queryrole = "student";
        }
        return this.querytype;
      });
    },
    getdata(querytype, queryrole) {
      GETSTATISTICS(querytype, queryrole, this.username, true).then((res) => {
        if (this.queryrole == "class") {
          this.projectlist = res.data.data;
          let title = "信息统计";
          let legend = ["平均成绩", "提交率"];
          let xAxis = [];
          let averagedata = [];
          let submitlvdata = [];
          let series = [];
          let tooltip = {
            trigger: "axis",
            formatter: "{b0}({a0}): {c0}<br />{b1}({a1}): {c1}%",
          };
          for (let item of this.projectlist) {
            xAxis.unshift(item.title);
            submitlvdata.unshift(item.submitlv);
            averagedata.unshift(item.averagegrade);
          }
          let temp = {};
          temp.name = "平均成绩";
          temp.type = "bar";
          temp.data = averagedata;
          temp.barWidth = "50%";
          series.push(temp);
          temp = {};
          temp.name = "提交率";
          temp.type = "line";
          (temp.smooth = true),
            (temp.yAxisIndex = 1),
            (temp.data = submitlvdata);
          series.push(temp);
          let yAxis = [
            {
              type: "value",
              name: "平均成绩",
              show: true,
              min: 0,
              max: 100,
              interval: 20,
              splitLine: { show: false },
              axisLine: {
                lineStyle: {
                  color: "#5e859e",
                  width: 2,
                },
              },
            },
            {
              type: "value",
              name: "提交率",
              min: 0,
              max: 100,
              interval: 20,
              splitLine: { show: false },
              axisLabel: {
                formatter: "{value} %",
              },
              axisLine: {
                lineStyle: {
                  color: "#5e859e", //纵坐标轴和字体颜色
                  width: 2,
                },
              },
            },
          ];
          this.myEcharts("main", title, tooltip, legend, xAxis, yAxis, series);
        } else {
          // console.log(res.data.data)
          this.studentlist = res.data.data;
        }
      });
    },
    selecthandle(index) {
      if (index == 1) {
        this.activeIndex = "1";
      } else {
        this.activeIndex = "2";
      }
      this.getclass();
    },
    myEcharts(dom, title, tooltip, legend, xAxis, yAxis, series) {
      // 基于准备好的dom，初始化echarts实例
      let myChart = echarts.init(document.getElementById(dom));

      // 指定图表的配置项和数据
      let option = {
        title: {
          text: title,
        },
        tooltip: tooltip,
        legend: {
          data: legend,
        },
        xAxis: [
          {
            type: "category",
            data: xAxis,
            axisPointer: {
              type: "shadow",
            },
            /* axisLabel: { //X轴文字竖着显示
               interval: 0,
               formatter:function(value)
               {
                   return value.split("").join("\n");
               }
            }*/

            axisLabel: {
              //X轴文字倾斜显示
              interval: 0,
              rotate: "-25",
            },
          },
        ],
        yAxis: yAxis,
        series: series,
      };

      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option);
    },
    projectinfo(EXPID) {
      SEARCHSUBMITLIST(EXPID, "all").then((res) => {
        let data = res.data.submitlist;
        for (let item of data) {
          if (item.grade == "") {
            item.grade = 0;
          }
        }
        this.projectrecord = data;
        this.projectdialogVisible = true;
        // console.log(res.data.submitlist);
      });
    },
    getInfo(STID) {
      GETALLRECORDS(STID).then((res) => {
        this.recorddialogVisible = true;
        let data = res.data.data;
        let title = "";
        let legend = ["成绩"];
        let xAxis = data.titles;
        let gradedata = data.grades;
        let series = [];
        let tooltip = {
          trigger: "axis",
          formatter: "{b0}({a0}): {c0}",
        };
        let yAxis={
              type: "value",
              name: "成绩",
              show: true,
              min: 0,
              max: 100,
              interval: 20,
              splitLine: { show: false },
              axisLine: {
                lineStyle: {
                  color: "#5e859e",
                  width: 2,
                },
              },
            };
        let temp = {};
        temp.name = "成绩";
        temp.type = "bar";
        temp.data = gradedata;
        temp.barWidth = "50%";
        series.push(temp);
        setTimeout(() => {
        this.myEcharts("everyrecord", title, tooltip, legend, xAxis,yAxis,series);
        }, 1);
      });
    },
  },
  watch: {
    querytype(val) {
      //   console.log(val, this.queryrole);
      this.getdata(val, this.queryrole);
    },
  },
};
</script>
<style lang='less' scoped>
.el-container {
  position: absolute;
  left: 0;
  top: 60px;
}
.el-main {
  width: calc(100vw - 200px);
}
.el-aside {
  background: none;
}
.el-menu-vertical-demo {
  height: 100%;
}

.el-col {
  height: 24vh;
  margin-bottom: 30px;
}

.el-card {
  height: 100%;
  min-height: 83%;
}
.el-card > .el-card__body {
  height: 100%;
}
.title {
  display: -webkit-box; /*作为弹性伸缩盒子模型显示*/
  -webkit-line-clamp: 1; /*显示的行数；如果要设置2行加...则设置为2*/
  overflow: hidden; /*超出的文本隐藏*/
  text-overflow: ellipsis; /* 溢出用省略号*/
  -webkit-box-orient: vertical; /*伸缩盒子的子元素排列：从上到下*/
  font-weight: 700;
  cursor: pointer;
}
.title:hover {
  color: #606266;
}
.head {
  position: relative;
}
.info {
  position: absolute;
  right: 0;
  top: 0;
  color: #606266;
}
.item {
  margin-bottom: 15px;
  font-size: 14px;
  color: #606266;
  white-space: nowrap;
}
.pubclass {
  float: right;
}
.switchbtn {
  position: absolute;
  right: 0;
  top: -25%;
}
</style>