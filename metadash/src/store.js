import Vue from 'vue'
import Vuex from 'vuex'
import _ from 'lodash'

Vue.use(Vuex)

let _changedConfigs = {} // XXX: ugly

function retriveErrMsg (err) {
  if (err.response) {
    if (err.response && err.response.data.message) {
      return Promise.reject(err.response.data)
    }
    return Promise.reject(err)
  }
}

function filterAPI (response) {
  if (response.status < 200 || response.status > 210) {
    if (response.data.message) {
      return Promise.reject(response.data)
    }
    return Promise.reject({
      message: JSON.stringify(response)
    })
  }
  return response.data
}

const store = new Vuex.Store({
  state: {
    configs: {},
    entities: {},
    alerts: [],
    username: null,
    role: 'anonymous'
  },
  actions: {
    login ({state}, {username, password, method, ignoreAPIError}) {
      return Vue.mdAPI.post('/login', {
        username: username,
        password: password,
        method: method || 'local'
      }, {
        ignoreAPIError: ignoreAPIError || false
      })
        .catch(retriveErrMsg)
        .then(filterAPI)
        .then(data => {
          state.username = data.username
          state.role = data.role
          return data
        })
    },
    logout ({state}) {
      return Vue.mdAPI.get('/logout')
        .catch(retriveErrMsg)
        .then(filterAPI)
        .then(data => {
          state.username = data.username
          state.role = data.role
          return data
        })
    },
    fetchMe ({state}) {
      return Vue.mdAPI.get('/me')
        .catch(retriveErrMsg)
        .then(filterAPI)
        .then(data => {
          state.username = data.username
          state.role = data.role
          return data
        })
    },
    fetchConfigs ({state}) {
      return Vue.mdAPI.get('/configs/')
        .catch(retriveErrMsg)
        .then(filterAPI)
        .then(data => data.data)
        .then(data => {
          state.configs = data
          for (let config of state.configs) {
            if (!config.nullable && !config.value) {
              config.error = "Can't be empty"
            }
          }
          return data
        })
    },
    saveConfigs: _.debounce(function ({state, dispatch}) {
      let configsToSubmit = _changedConfigs
      _changedConfigs = {}
      for (let key in configsToSubmit) {
        let value = configsToSubmit[key]
        let config = _.find(state.configs, {key})
        Vue.mdAPI.put('/configs/' + key, {
          value: value
        }).then(() => {
          config.value = value
          config.error = null
        }).catch((errRes) => {
          config.error = 'Failed to save due to ' + errRes
        }).then(() => {
          if (!config.nullable && !config.value) {
            config.error = "Can't be empty" // TODO: move to a standalone file for config handling
          }
        })
      }
    }, 1000),
    updateConfig ({state, dispatch}, {key, value}) {
      _changedConfigs[key] = value
      dispatch('saveConfigs')
    },
    newAlert ({state, dispatch}, {text, level}) {
      state.alerts.push({ type: level, msg: text, alert: true })
    }
  },
  getters: {
    getConfig: (state) => (key) => {
      return _.find(state.configs, {key: key})
    }
  },
  mutations: {
    registEntity (state, entity) {
      if (!entity.uuid) {
        throw new Error('Received an Entity with no UUID! ' + entity)
      }
      state.entities[entity.uuid] = entity
    },
    updateEntity (state, entity) {
      if (!entity.uuid) {
        throw new Error('Received an Entity with no UUID! ' + entity)
      }
      Object.assign(state.entities[entity.uuid], entity)
    }
  }
})

export default store
