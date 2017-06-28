<template>
  <pf-layout id="app" :icons="true">
    <pf-notifications ref="notifications"> </pf-notifications>
    <pf-drawer :hidden="!showNotificationDrawer" :allow-expand="true" title="Notifications">
      <pf-drawer-group title="Recent Activities" action="Mark All Read">
        <pf-drawer-notification message="User xxx triggerd jobs">
        </pf-drawer-notification>
      </pf-drawer-group>
      <pf-drawer-group title="Running tasks">
        <pf-drawer-notification message="Background Celery tasks will be shown here">
        </pf-drawer-notification>
      </pf-drawer-group>
      <pf-drawer-group title="Server Info">
        <pf-drawer-notification message="Metadash v0.1 Running">
        </pf-drawer-notification>
      </pf-drawer-group>
    </pf-drawer>
    <bs-modal title="User Info" effect="fade" width="800" :value="showTopModal" @closed="showTopModal = false">
      <user v-show="loggedIn" slot="modal-body" class="modal-body" @success="showTopModal = false"> </user>
      <login v-show="!loggedIn" slot="modal-body" class="modal-body" @success="showTopModal = false"> </login>
      <div slot="modal-footer">
        <div v-if="loginModalInfo" class="alert alert-danger">
          <span class="pficon pficon-error-circle-o"></span>
          <strong> {{ loginModalInfo }} </strong>
        </div>
      </div>
    </bs-modal>
    <ul slot="utility-menu" class="nav navbar-nav navbar-right">
      <li>
        <a class="nav-item-iconic"> <span title="Reload Current Page" class="fa fa-refresh"></span> </a>
      </li>
      <li>
        <a class="nav-item-iconic" @click="notificationDrawer(!showNotificationDrawer)"> <span title="Notifications" class="fa fa-bell"></span> </a>
      </li>
      <li>
        <a class="nav-item-iconic" @click="userModal(true)"> <span title="User Info" class="fa fa-user"></span> <b>{{ username }}</b> </a>
      </li>
    </ul>
    <router-link slot="brand" to="/" :exact="true" class="navbar-brand">
      <span class="navbar-brand-name">Metadash</span>
    </router-link>

    <template slot="vertical-menu">
      <router-link tag="li" class="list-group-item" active-class="active" to="/dashboard">
        <a>
          <span class="fa fa-dashboard" title="Dashboard"></span>
          <span class="list-group-item-value">Dashboard</span>
        </a>
      </router-link>
      <router-link v-for="plugin in plugins" :key="plugin.path" tag="li" class="list-group-item" active-class="active" :to="plugin.path">
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
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
export default {
  name: 'app',
  props: ['plugins'],
  components: { Login, User },
  data () {
    return {
      showNotificationDrawer: false,
      showTopModal: false,
      loginModalInfo: '',
      errorModalInfo: ''
    }
  },
  methods: {
    userModal (show, info) {
      this.showTopModal = show
      this.loginModalInfo = info
    },
    notificationDrawer (show, info) {
      this.showNotificationDrawer = show
    },
    makeToast (text, level) {
      this.$refs.notifications.add(text, level)
    }
  },
  created () {
    let vm = this
    Vue.http.interceptors.push((request, next) => {
      NProgress.start()
      next((response) => {
        NProgress.done()
        if (response.status === 401) {
          vm.userModal(true, "You don'e have required permission")
          return response
        } else if (response.status === 202) {
          response.json().then((data) => {
            this.makeToast(data.message, 'info')
          }, () => {
            this.makeToast(response.body || 'No Response', 'warning')  // TODO: Danger!!!
          })
        } else if (!response.ok) {
          response.json().then((data) => {
            if (data.message) {
              this.makeToast(data.message, 'danger')
            } else {
              this.makeToast('Unknown Error: ' + JSON.stringify(data), 'danger')
            }
          }, () => {
            this.makeToast(response.body || 'No Response', 'danger')  // TODO: Danger!!!
          })
          return response
        }
        return response
      })
    })
  },
  mounted () {
  },
  computed: {
    loggedIn () {
      return !!this.$store.state.username
    },
    username () {
      return this.$store.state.username || 'anonymous'
    }
  }
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 15px;
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
