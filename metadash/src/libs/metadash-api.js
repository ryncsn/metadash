// Extend Vue-resource, apply interceptor only to request made using
// given helpers
// TODO: make something like sub-resource
// an resource extention that can have a standalone set of interceptors etc
import Vue from 'vue'

class API {
  constructor ({
    apiPrefix
  }) {
    this.apiPrefix = apiPrefix || '/api'
    this.interceptors = []

    this.interceptors.push = (...args) => {
      for (let handler of args) {
        Vue.http.interceptors.push((request, next) => {
          if (request.apiRequestPrefix === this.apiPrefix) {  // Only intercept relative URL
            handler(request, next)
          }
        })
      }
      return Array.prototype.push.apply(this.interceptors, ...args)
    }

    let APIRequest = (method, url, options, ...args) => {
      options = Object.assign(options || {}, {
        apiRequestPrefix: this.apiPrefix
      })
      return Vue.http[method](this.getAPIUrl(url), ...args, options)
    }

    ['get', 'delete', 'head', 'jsonp'].forEach(method => {
      this[method] = function (url, options) {
        return APIRequest(method, url, options)
      }
    });

    ['post', 'put', 'patch'].forEach(method => {
      this[method] = function (url, body, options) {
        return APIRequest(method, url, options, body)
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
    if (!Vue.http) {
      throw Error('Vue-resource not installed.')
    }

    Vue.mdAPI = api
    Vue.prototype.$mdAPI = api
  }
}

export default MetadashAPIInstaller
