# 基于Axios的自定义通用网络请求封装

封装代码如下：

```javascript
/** axios 请求封装 */

// 引入axios
import axios from 'axios'

// baseURL选项，表示请求URL公共部分
const BASE_URL = "/dev-api"

// 创建axios实例
const instance = axios.create({
    baseURL: BASE_URL,
    // 超时时间
    timeout: 1000
});

// 请求拦截器
instance.interceptors.request.use(config => {
    // 在发送请求之前做些什么,包括请求配置
    config.headers['Authorization'] = config.isToken ? 'Bearer ' + localStorage.getItem('token') : null;
    config.headers['Content-Type'] = config.headers['Content-Type'] || 'application/json;charset=UTF-8'; // 默认请求头
    config.timeout = config.timeout || 1000; // 请求超时时间
    // 加载动画
    console.log("[loading]网络请求中...请稍后！");
    return config
}, error => {
    // 对请求错误做些什么
    console.log("网络请求错误！", error);
    return Promise.reject(error)
})

// 响应拦截器
instance.interceptors.response.use(response => {
    // 对响应数据做点什么
    console.log("response:", response);
    console.log("[关闭loading]网络请求成功！");
    return response
}, error => {
    // 对响应错误做点什么
    let { message } = error;
    if (message == "Network Error") {
        message = "后端接口连接异常";
    } else if (message.includes("timeout")) {
        message = "系统接口请求超时";
    } else if (message.includes("Request failed with status code")) {
        message = "系统接口" + message.substr(message.length - 3) + "异常";
    }
    console.log("[关闭loading]网络请求失败！", message);
    return Promise.reject(error)
})


/** 
 * 请求导出方法
 * @param {object} params  请求参数
 * @param {string} [params.headers] 请求头
 * @param {string} params.url 请求地址
 * @param {string} [params.method] 请求方法
 * @param {string} [params.data] 请求参数
 * @param {string} [params.params] 请求参数
 * @param {string} [params.headers] 请求头
 * @param {string} [params.timeout] 请求超时时间
 * @param {string} [params.isToken] 是否需要token
 * @return {Promise} 返回Promise对象
 * */
export const request = (params) => {
    return new Promise((resolve, reject) => {
        instance(params).then(res => {
            resolve(res.data)
        })
            .catch(err => {
                reject(err)
            })
    })
}

```


