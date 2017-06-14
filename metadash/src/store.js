import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
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
    }
  }
})

export default store
