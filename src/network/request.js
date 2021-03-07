import axios from 'axios'
import { Loading } from 'element-ui';

export function request(config, isloading = false) {
    let loadingInstance;
    const instance = axios.create({
        baseURL: "/api",
        timeout: 10000
    })
    instance.interceptors.request.use(config => {
        config.headers.Authorzation = window.sessionStorage.getItem('token')
        if (isloading) {
            loadingInstance = Loading.service({
                lock: true,
                text: 'Loading',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)'
            });
        }
        return config
    }, err => {
        console.log(err)
    })
    instance.interceptors.response.use(res => {
        if (isloading) {
            loadingInstance.close();
        }
        return res
    }, err => {
        console.log(err)
    })

    return instance(config)
}