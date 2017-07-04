import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
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
        .then(data => {
          state.configs = data
        })
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
