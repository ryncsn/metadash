<template>
  <v-app>
    <v-container fluid>
      <v-layout v-if="appReady">
        <v-navigation-drawer
          fixed dark app
          id="app"
          v-model="pluginsListDrawer"
          mini-variant.sync="mini"
          :clipped="$vuetify.breakpoint.lgAndUp"
          >
          <v-list>
            <v-list-tile @click="" :to="'/dashboard'">
              <v-list-tile-action>
                <v-icon>dashboard</v-icon>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>Dashboard</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
            <template v-for="item in plugins">
              <v-list-tile @click="" :key="item.title" :to="item.path">
                <v-list-tile-action>
                  <v-icon>{{ item.icon }}</v-icon>
                </v-list-tile-action>
                <v-list-tile-content>
                  <v-list-tile-title>
                    {{ item.title }}
                  </v-list-tile-title>
                </v-list-tile-content>
              </v-list-tile>
            </template>
            <v-list-tile @click="" :to="'/config'">
              <v-list-tile-action>
                <v-icon>settings</v-icon>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>Config</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-navigation-drawer>
        <v-toolbar
          dark fixed app
          color="blue-grey darken-1"
          :clipped-left="$vuetify.breakpoint.lgAndUp"
          >
          <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
            <v-tooltip bottom>
              <v-toolbar-side-icon slot="activator" @click.stop="pluginsListDrawer = !pluginsListDrawer"></v-toolbar-side-icon>
              <span>Open Plugin List</span>
            </v-tooltip>
            <span class="hidden-sm-and-down">Metadash</span>
          </v-toolbar-title>
          <v-spacer></v-spacer>
          <v-tooltip bottom>
            <v-menu
              offset-y
              :close-on-content-click="false"
              max-width="160"
              nudge-left="60"
              slot="activator"
              >
              <v-btn icon slot="activator">
                <v-icon>apps</v-icon>
              </v-btn>
              <v-card>
                <v-list>
                  <v-tooltip bottom>
                    <v-btn slot="activator" icon :to="'/dashboard'">
                      <v-icon>dashboard</v-icon>
                    </v-btn>
                    <span>Dashboard</span>
                  </v-tooltip>
                  <v-tooltip v-for="item in plugins" :key="item.title" bottom>
                    <v-btn slot="activator" icon :to="item.path">
                      <v-icon>{{ item.icon }}</v-icon>
                    </v-btn>
                    <span>{{ item.title }}</span>
                  </v-tooltip>
                  <v-tooltip bottom>
                    <v-btn slot="activator" icon :to="'/config'">
                      <v-icon>settings</v-icon>
                    </v-btn>
                    <span>Config</span>
                  </v-tooltip>
                </v-list>
              </v-card>
            </v-menu>
            <span>Display App List</span>
          </v-tooltip>
          <v-tooltip bottom>
            <v-menu
              offset-y
              :close-on-content-click="false"
              :nudge-width="expandNotificationDrawer ? 800 : 200"
              :nudge-left="expandNotificationDrawer ? 650 : 100"
              slot="activator"
              >
              <v-badge slot="activator" overlap color="red">
                <span v-if="NoticeNum > 0" slot="badge">{{ NoticeNum }}</span>
                <v-btn icon >
                  <v-icon>notifications</v-icon>
                </v-btn>
              </v-badge>
              <v-card>
                <v-card-title>
                  <v-btn icon @click="expandNotificationDrawer = !expandNotificationDrawer">
                    <v-icon>swap_horiz</v-icon>
                  </v-btn>
                  <v-btn icon @click="noticeDialog = !noticeDialog">
                    <v-icon>fullscreen</v-icon>
                  </v-btn>
                </v-card-title>
                <Notices :metadashVersion="metadashVersion"/>
              </v-card>
            </v-menu>
            <span>Open Notice List</span>
          </v-tooltip>
          <v-tooltip bottom>
            <v-btn icon slot="activator" @click="refreshCurrentPage">
              <v-icon>refresh</v-icon>
            </v-btn>
            <span>Refresh Page</span>
          </v-tooltip>
          <v-tooltip bottom>
            <v-btn slot="activator" v-show="!loggedIn" icon @click.stop="showLoginDialog = !showLoginDialog">
              <v-icon>account_circle</v-icon>
            </v-btn>
            <span>Login</span>
          </v-tooltip>
          <v-tooltip bottom>
            <v-menu slot="activator" bottom left v-show="loggedIn" offset-y>
              <v-avatar slot="activator" class="cyan darken-1" :size="40">
                <span class="white--text headline">{{ username.slice(0, 1).toUpperCase() }}</span>
              </v-avatar>
              <v-list dense>
                <v-list-tile @click.stop="showLogoutDialog = !showLogoutDialog">
                  <v-list-tile-title>Logout</v-list-tile-title>
                </v-list-tile>
              </v-list>
            </v-menu>
            <span>Account Actions</span>
          </v-tooltip>
        </v-toolbar>
        <v-content v-if="appReady">
          <Alert/>
          <router-view ref="currentRouteComponent"></router-view>
        </v-content>
        <v-dialog v-model="showLoginDialog" max-width="800px">
          <Login @success="showLoginDialog = false"/>
        </v-dialog>
        <v-dialog v-model="showLogoutDialog" max-width="800px">
          <User @success="showLogoutDialog = false">
          </User>
        </v-dialog>
        <v-dialog
          v-model="noticeDialog"
          fullscreen
          transition="dialog-bottom-transition"
          :overlay="false"
          scrollable
          >
          <v-card tile>
            <v-toolbar card dark color="primary">
              <v-btn icon @click.native="noticeDialog = false" dark>
                <v-icon>close</v-icon>
              </v-btn>
            </v-toolbar>
            <v-card-text>
              <Notices :metadashVersion="metadashVersion"/>
            </v-card-text>
          </v-card>
        </v-dialog>
        <v-btn
          fab
          bottom
          right
          color="white"
          fixed
          v-if="loading"
          >
          <v-progress-circular indeterminate :size="40" color="primary">
          </v-progress-circular>
        </v-btn>
      </v-layout>
      <Splash v-else/>
    </v-container>
  </v-app>
</template>

<script>
import Vue from 'vue'
import version from './libs/metadash-version.js'
import User from '@/components/User.vue'
import Login from '@/components/Login.vue'
import Alert from '@/components/Alert.vue'
import Splash from '@/components/Splash.vue'
import Notices from '@/components/Notices.vue'
import _ from 'lodash'
export default {
  name: 'app',
  props: ['plugins'],
  components: { Login, User, Alert, Notices, Splash },
  data () {
    return {
      metadashVersion: `Metadash ${version} Running`,
      appReady: false,
      loading: false,
      pluginsListDrawer: false,
      showNotificationDrawer: false,
      expandNotificationDrawer: false,
      noticeDialog: false,
      showLoginDialog: false,
      showLogoutDialog: false,
      showTopModal: false,
      loginModalInfo: '',
      errorModalInfo: ''
    }
  },
  methods: {
    makeToast (text, level) {
      this.$store.dispatch('newAlert', { text: text, level: level })
    },
    refreshCurrentPage () {
      if (_.isFunction(this.$refs.currentRouteComponent.refresh)) {
        this.$refs.currentRouteComponent.refresh()
      } else {
        this.makeToast("This page or this plugin doesn't support inpage refreshing, please reload the page manually.")
      }
    }
  },
  created () {
    Vue.mdAPI.interceptors.request.use(config => {
      this.loading = true
      return config
    }, error => {
      return Promise.reject(error)
    })
    Vue.mdAPI.interceptors.response.use(response => {
      this.loading = false
      if (response.config.ignoreAPIError) {
        return response
      } else if (response.status === 401) {
        this.makeToast('You don\'t have required permission', 'error')
      } else if (response.status === 202) {
        response.data.message && (
          this.makeToast(response.data.message, 'info') ||
          this.makeToast(JSON.stringify(response.data), 'warning'))
      } else if (response.status < 300 && response.status >= 200) {
        // Do nothing
      } else {
        response.data.message && (
          this.makeToast(response.data.message, 'error') ||
          this.makeToast(JSON.stringify(response.data), 'error'))
      }
      return response
    }, error => {
      // Following code only work when interacting with Metadash's API
      this.loading = false
      if (error.response) {
        let response = error.response
        if (response.config.ignoreAPIError) {
          return Promise.reject(error)
        } else {
          response.data.message && (
            this.makeToast(response.data.message, 'error')) ||
            this.makeToast(JSON.stringify(error.message), 'error')
        }
      } else {
        this.makeToast(error.message, 'error')
      }
      return Promise.reject(error)
    })
    this.$store.dispatch('fetchMe').then(() =>
      this.$store.dispatch('fetchConfigs')
    ).then(() => { this.appReady = true })
  },
  mounted () {
  },
  computed: {
    loggedIn () {
      return !!this.$store.state.username
    },
    NoticeNum () {
      return 0 // TODO: need count all the messages
    },
    username () {
      return this.$store.state.username || 'anonymous'
    }
  }
}
</script>

<style>
</style>
