import axios from 'axios'

// 创建Axios实例
const request = axios.create({
  baseURL: 'http://localhost:5000/api', // 后端API基础URL
  timeout: 10000, // 请求超时时间
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 可以在这里添加请求头，如Token
    // config.headers.Authorization = `Bearer ${localStorage.getItem('token')}`
    return config
  },
  error => {
    // 处理请求错误
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    // 处理响应数据
    const res = response.data
    
    // 如果返回的success为false，则抛出错误
    if (!res.success) {
      return Promise.reject(new Error(res.message || '请求失败'))
    }
    
    return res.data
  },
  error => {
    // 处理响应错误
    console.error('响应错误:', error)
    
    // 可以根据错误状态码进行不同的处理
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 未授权，跳转到登录页
          break
        case 403:
          // 禁止访问
          break
        case 404:
          // 资源未找到
          break
        case 500:
          // 服务器内部错误
          break
        default:
          // 其他错误
          break
      }
    }
    
    return Promise.reject(error)
  }
)

export default request
