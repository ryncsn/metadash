<template>
  <v-layout align-center justify-center>
    <v-flex>
      <v-card class="elevation-12">
        <v-toolbar dark color="primary">
          <v-toolbar-title>Login form</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-card-text>
          <v-form>
            <v-text-field
              prepend-icon="person"
              name="username"
              label="Login"
              type="text"
              v-model="username"
            ></v-text-field>
            <v-text-field
              prepend-icon="lock"
              name="password"
              label="Password"
              type="password"
              v-model="password"
              :rules="[check_error]"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-progress-linear v-show="loginInProgress" :indeterminate="true"></v-progress-linear>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="login" :disabled="loginInProgress">Login</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'login',
  data () {
    return {
      username: '',
      password: '',
      error: '',
      loginInProgress: false
    }
  },
  methods: {
    login () {
      this.loginInProgress = true
      this.$store.dispatch('login', {
        username: this.username,
        password: this.password
      })
        .then(() => {
          this.$emit('success')
        }, () => {
          this.$emit('failed')
          this.error = 'Invalid username or password'
        })
        .catch(() => {}).then(() => { this.loginInProgress = false })
    },
    check_error () {
      if (this.error === '') {
        return true
      } else {
        return this.error
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
