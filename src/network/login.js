import {request} from './request';
import md5 from 'js-md5';

export function Login(username,password){
    let param = new URLSearchParams()
    param.append('username', username)
    param.append('password', md5(password))   
    return request({
        url:'/login',
        method:'post',
        // data:{
        //     'username':username,
        //     'password':md5(password)
        // },
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })
}
export function Reset(username,cardcode){
    let param = new URLSearchParams()
    param.append('username', username)
    param.append('cardcode', cardcode)   
    return request({
        url:'/forget',
        method:'post',
        // data:{
        //     'username':username,
        //     'password':md5(password)
        // },
        data:param,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
    })
}