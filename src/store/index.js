import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    path:'/home/first',
    username:'',
    type:-1,
    name:''
  },
  mutations: {
    setpath(state,payload){
      state.path=payload
    },
    setusername(state,payload){
      state.username=payload
    },
    settype(state,payload){
      state.type=payload
    },
    setname(state,payload){
      state.name=payload
    }
  },
  actions: {
  },
  modules: {
  }
})
