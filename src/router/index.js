import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store'

Vue.use(VueRouter)

const Login = () => import("@/views/login")
const Home = () => import("@/views/home")
const First = () => import("@/views/Home/first")
const Profile = () => import("@/views/Home/profile")
const Projects = () => import("@/views/Home/projects")
const Statistics = () => import("@/views/Home/teacher/statistics")
const Admins = () => import("@/views/Management/admins")
const Students = () => import("@/views/Management/students")
const Teachers = () => import("@/views/Management/teachers")
const Classes = () => import("@/views/Management/classes")
const Experienments = () => import("@/views/Management/experienments")
const ExperienmentDisplay = () => import("@/views/Home/teacher/experienmentDisplay")
const ExperienmentFix = () => import("@/views/Home/teacher/experienmentFix")
const ExperienmentsFix = () => import("@/views/Management/experienmentsFix")
const Detail = () => import("@/views/Home/student/detail")
const EditProject = () => import("@/views/Home/teacher/editproject")
const AddProject = () => import("@/views/Home/teacher/addproject")
const CorrectProject = () => import("@/views/Home/teacher/correctproject")
const AddAnswer = () => import("@/views/Home/teacher/addanswer")
const CorrectAll = () => import("@/views/Home/teacher/correctall")
const Addexdemo = () => import("@/views/Management/addexdemo")
const Editexdemo = () => import("@/views/Management/editexdemo")
const Showexdemo = () => import("@/views/Home/teacher/showexdemo")


const routes = [
  {
    path: '',
    redirect: "/login"
  },
  {
    path: '/login',
    component: Login
  },
  {
    path: '/home',
    component: Home,
    children: [
      {
        path: '',
        redirect: "/home/projects"
      },
      {
        path: '/home/first',
        component: First
      },
      {
        path: '/home/projects',
        component: Projects
      },
      {
        path: '/home/profile',
        component: Profile
      },
      {
        path: '/home/statistics',
        component: Statistics
      },
      {
        path: '/home/teachers',
        component: Teachers
      },
      {
        path: '/home/admins',
        component: Admins
      },
      {
        path: '/home/students',
        component: Students
      },
      {
        path: '/home/classes',
        component: Classes
      },
      {
        path: '/home/experienments',
        component: Experienments
      },
      {
        path: '/home/experienmentdisplay',
        component: ExperienmentDisplay
      },
      {
        path: '/home/experienmentfix',
        component: ExperienmentFix
      },
      {
        path: '/home/experienmentsfix',
        component: ExperienmentsFix
      },
      {
        path: '/home/detail',
        component: Detail
      },
      {
        path: '/home/editproject',
        component: EditProject
      },
      {
        path: '/home/addproject',
        component: AddProject
      },
      {
        path: '/home/correctproject',
        component: CorrectProject
      },
      {
        path: '/home/addanswer',
        component: AddAnswer
      },
      {
        path: '/home/correcting',
        component: CorrectAll
      },
      {
        path: '/home/addexdemo',
        component: Addexdemo
      },
      {
        path: '/home/editexdemo',
        component: Editexdemo
      },
      {
        path: '/home/showexdemo',
        component: Showexdemo
      },

    ]
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

const routerPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return routerPush.call(this, location).catch(error => error)
}
router.beforeEach((to, from, next) => {
  if (to.path === '/login') return next()
  const tokenStr = window.sessionStorage.getItem('token')
  if (!tokenStr) return next('/login')
  // window.sessionStorage.setItem('path',to.path)
  store.commit('setpath', to.path)
  next()
})

export default router
