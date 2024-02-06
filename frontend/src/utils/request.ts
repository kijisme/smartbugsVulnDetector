import axios from 'axios';
import NProgress from 'nprogress';
// @ts-ignore
import 'nprogress/nprogress.css';
import { serverUrl, getToken } from './tools';

const instance = axios.create({
    baseURL: serverUrl, // 请求的基础地址
    timeout: 5000,
    withCredentials: true,
  });

// 拦截器
// Add a request interceptor，发起请求之前执行
instance.interceptors.request.use(
  function (config) {
    config.headers.Bearer = getToken();
    NProgress.start(); // 启动loading
    return config;
  },
  function (error) {
    // Do something with request error
    return Promise.reject(error);
  }
);

// Add a response interceptor，请求返会之后执行
instance.interceptors.response.use(
  function (response) {
    NProgress.done();
    return response;
  },
  function (error) {
    NProgress.done(); // 关闭loading
   
    return Promise.reject(error);
  }
);


// 封装get
export const get = (url: string, params: any = {}) => instance.get(url, { params }).then((res) => res.data);

//封装post
export const post = (url: string, data: any = {}) => instance.post(url, data).then((res) => res.data);

//封装put
export const put = (url: string, data: any = {}) => instance.put(url, data).then((res) => res.data);

//封装patch
export const patch = (url: string, data: any = {}) => instance.patch(url, data).then((res) => res.data);

//封装delete请求
export const del = (url: string) => instance.delete(url).then((res) => res.data);