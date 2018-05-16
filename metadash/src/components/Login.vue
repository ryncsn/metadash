<template>
  <v-card class="elevation-12">
    <v-progress-linear v-show="loginInProgress" :indeterminate="true"></v-progress-linear>
    <v-card-title>
      <span class="headline">Login</span>
    </v-card-title>
    <v-card-text>
      <v-form lazy-validation v-model="valid">
        <v-text-field
          prepend-icon="person"
          type="text"
          name="username"
          label="Username"
          v-model="username"
          :rules="usernameRules"
          @keyup.enter="login"
          required
          ></v-text-field>
        <v-text-field
          prepend-icon="vpn_key"
          type="password"
          name="password"
          label="Password"
          v-model="password"
          :rules="passwordRules"
          @keyup.enter="login"
          required
          ></v-text-field>
        <v-select
          prepend-icon="lock"
          :items="loginMethods"
          v-model="loginMethod"
          name="loginMethod"
          label="Authentication Method"
          required
          ></v-select>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
        flat large
        color="primary"
        @click="login"
        :disabled="!valid || loginInProgress"
        > Login </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'login',
  data () {
    return {
      valid: false,
      username: '',
      usernameRules: [
        v => !!v || 'Username is required'
      ],
      password: '',
      passwordRules: [
        v => !!v || 'Password is required'
      ],
      loginMethod: 'local',
      loginMethods: [
        'local',
        'ldap'
      ],
      loginInProgress: false
    }
  },
  methods: {
    login () {
      this.loginInProgress = true
      this.$store.dispatch('login', {
        username: this.username,
        password: this.password,
        method: this.loginMethod
      })
        .then(() => {
          this.$emit('success')
        }, () => {
          this.$emit('failed')
        })
        .catch(() => {})
        .then(() => {
          this.loginInProgress = false
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
