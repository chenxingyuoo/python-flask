'use strict'

import axios from 'axios'
import qs from 'qs'
import { message } from 'antd';

const successCode = 200
const failCode = 500
const notAuthCode = 1000

// 创建axios实例
const service = axios.create({
  baseURL: process.env.NODE_ENV === 'development' ? '/api' : ''
})


// 添加一个请求拦截器
service.interceptors.request.use(function (config) {
  // Do something before request is sent
  return config;
}, function (error) {
  // Do something with request error
  return Promise.reject(error);
});

// 添加一个响应拦截器
service.interceptors.response.use(function (response) {
  // Do something with response data
  if (response.status >= 200 && response.status <= 300) {
    if (response.data.code === successCode) {
      return response.data
    }

    if (response.data.code === failCode) {
      message.warning(response.data.message)
      return Promise.reject(response)
    }

    if (response.data.code === notAuthCode) {
      window.location.hash = '#/login'
      return Promise.reject(response)
    }
  }
}, function (error) {
  if (error.response && error.response.status >= 400) {
    message.error('网络发生错误')
  }
  // Do something with response error
  return Promise.reject(error);
});


/**
 * 统一get请求入口
 * @param {object} opts 请求参数对象
 * @returns {Promise<AxiosResponse<any>>}
 */
service.get = (opts) => {
  return service({
    url: opts.url,
    method: 'GET',
    params: opts.data
  })
}

/**
 * 统一post请求入口
 * @param {object} opts 请求参数对象
 * @returns {Promise<AxiosResponse<any>>}
 */
service.post = (opts) => {
  return service({
    url: opts.url,
    method: 'POST',
    data: opts.data,
    headers: {
      'Content-Type': 'application/json;charset=UTF-8'
    }
  })
}

export default service