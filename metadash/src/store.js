import Vue from 'vue'
import Vuex from 'vuex'
import _ from 'lodash'

Vue.use(Vuex)

let _changedConfigs = {} // XXX: ugly

const store = new Vuex.Store({
  state: {
    configs: {},
    entities: {},
    alerts: [],
    username: null,
    role: 'anonymous'
  },
  actions: {
    login ({state}, {username, password, method}) {
      return Vue.mdAPI.post('/login', {
        username: username,
        password: password,
        method: method || 'local'
      }).then(res => res.json())
        .then(data => {
          state.username = data.username
          state.role = data.role
        })
    },
    logout ({state}) {
      return Vue.mdAPI.get('/logout')
        .then(res => res.json())
        .then(data => {
          state.username = data.username
          state.role = data.role
        })
    },
    fetchMe ({state}) {
      return Vue.mdAPI.get('/me')
        .then(res => res.json())
        .then(data => {
          state.username = data.username
          state.role = data.role
        })
    },
    fetchConfigs ({state}) {
      return Vue.mdAPI.get('/configs/')
        .then(res => res.json())
        .then(data => data.data)
        .then(data => {
          state.configs = data
          for (let config of state.configs) {
            if (!config.nullable && !config.value) {
              config.error = "Can't be empty"
            }
          }
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
