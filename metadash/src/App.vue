<template>
  <pf-layout id="app" :icons="true">
    <bs-modal title="User Info" effect="fade" width="800" :value="showPersonalModal" @closed="showPersonalModal = false">
      <user v-show="loggedIn" slot="modal-body" class="modal-body" @success="showPersonalModal = false">
      </user>
      <login v-show="!loggedIn" slot="modal-body" class="modal-body" @success="showPersonalModal = false">
      </login>
      <div slot="modal-footer">
        <div v-if="modalInfo" class="alert alert-danger">
          <span class="pficon pficon-error-circle-o"></span>
          <strong> {{ modalInfo }} </strong>
        </div>
      </div>
    </bs-modal>
    <li slot="utility-menu">
      <a class="nav-item-iconic" @click="loginModal()">
        <span class="fa fa-user" title="User" data-toggle="modal" data-target=".bs-example-modal-sm"></span>
      </a>
    </li>
    <router-link slot="brand" to="/" :exact="true" class="navbar-brand">
      <span class="navbar-brand-name">Metadash</span>
    </router-link>

    <template slot="vertical-menu">
      <router-link tag="li" class="list-group-item" active-class="active" to="/dashboard" :exact="true">
        <a>
          <span class="fa fa-dashboard" title="Dashboard"></span>
          <span class="list-group-item-value">Dashboard</span>
        </a>
      </router-link>
      <router-link tag="li" class="list-group-item" active-class="active" to="/table" :exact="true">
        <a>
          <span class="fa fa-columns" title="Table"></span>
          <span class="list-group-item-value">Table</span>
        </a>
      </router-link>
      <router-link v-for="plugin in plugins" :key="plugin.path" tag="li" class="list-group-item" active-class="active" :to="plugin.path" :exact="true">
        <a>
          <span :title="plugin.title" v-html="plugin.icon"></span>
          <span class="list-group-item-value">{{plugin.title}}</span>
        </a>
      </router-link>
      <router-link tag="li" class="list-group-item" active-class="active" to="/config" :exact="true">
        <a>
          <span class="fa fa-gear" title="Config"></span>
          <span class="list-group-item-value">Config</span>
        </a>
      </router-link>
    </template>
    <keep-alive>
      <router-view></router-view>
    </keep-alive>
  </pf-layout>
</template>

<script>
import Vue from 'vue'
import Login from '@/components/Login.vue'
import User from '@/components/User.vue'
export default {
  name: 'app',
  props: ['plugins'],
  components: { Login, User },
  data () {
    return {
      showPersonalModal: false,
      modalInfo: ''
    }
  },
  methods: {
    loginModal (info) {
      this.showPersonalModal = !this.showPersonalModal
      this.modalInfo = info
    }
  },
  mounted () {
    let vm = this
    Vue.http.interceptors.push((request, next) => {
      next((response) => {
        if (response.status === 401) {
          vm.loginModal("You don'e have required permission")
        }
      })
    })
  },
  computed: {
    loggedIn () {
      return !!this.$store.state.username
    }
  }
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}

.navbar-pf-vertical .navbar-brand {
  font-size: 20px;
  line-height: 35px;
}

.navbar-brand-name,
.home .jumbotron h1 {
  background: -webkit-linear-gradient(#5399F9,#6df7ac);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  color: #5399F9;
}

/*
Fix for pattern fly side bar animation
 */
.nav-pf-vertical, .nav-pf-vertical a {
  -webkit-transition:width 300ms ease-in-out, height 300ms ease-in-out;
  -moz-transition:width 300ms ease-in-out, height 300ms ease-in-out;
  -o-transition:width 300ms ease-in-out, height 300ms ease-in-out;
  transition:width 300ms ease-in-out, height 300ms ease-in-out;
}

</style>
