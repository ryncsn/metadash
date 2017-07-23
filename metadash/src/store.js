import Vue from 'vue'
import Vuex from 'vuex'
import _ from 'lodash'

Vue.use(Vuex)

let _changedConfigs = {} // XXX: ugly

const store = new Vuex.Store({
  state: {
    configs: {},
    entities: {},
    username: null,
    role: 'anonymous'
  },
  actions: {
    login ({state}, {username, password}) {
      return Vue.http.post('/api/login', {
        username: username,
        password: password
      }).then(res => res.json())
        .then(data => {
          state.username = data.username
          state.role = data.role
        })
    },
    logout ({state}) {
      return Vue.http.get('/api/logout')
        .then(res => res.json())
        .then(data => {
          state.username = data.username
          state.role = data.role
        })
    },
    fetchMe ({state}) {
      return Vue.http.get('/api/me')
        .then(res => res.json())
        .then(data => {
          state.username = data.username
          state.role = data.role
        })
    },
    fetchConfigs ({state}) {
      return Vue.http.get('/api/configs')
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
        Vue.http.put('/api/configs/' + key, {
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
