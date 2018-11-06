// Apply interceptor only to request made using given helpers
import Vue from 'vue'
import axios from 'axios'

class API {
  constructor ({
    apiPrefix
  }) {
    this.apiPrefix = apiPrefix || '/api'
    this.axiosInstance = axios.create({
      baseURL: this.apiPrefix,
      headers: {
        'Content-Type': 'application/json;charset=UTF-8'
      }
    })
    this.interceptors = this.axiosInstance.interceptors

    let APIRequest = (method, path, {data, ...options}) => {
      return this.axiosInstance.request({
        url: path,
        method,
        data: data || {},  // GET require an empty data for header to work
        ...(options || {})
      })
    }

    ['get', 'delete', 'head'].forEach(method => {
      this[method] = function (path, options) {
        return APIRequest(method, path, {...(options || {})})
      }
    });

    ['post', 'put', 'patch'].forEach(method => {
      this[method] = function (path, data, options) {
        return APIRequest(method, path, {data: data, ...(options || {})})
      }
    })
  }

  getAPIUrl (relativeURL) {
    return this.apiPrefix + relativeURL
  }

  resource (...args) {
    throw Error('Not implemented')
  }
}

const MetadashAPIInstaller = {
  install () {
    let api = new API('/api')
    Vue.mdAPI = api
    Vue.prototype.$mdAPI = api
  }
}

export default MetadashAPIInstaller
