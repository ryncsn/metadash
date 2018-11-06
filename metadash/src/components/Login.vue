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
          :error="usernameError"
          :error-messages="usernameErrorMessages"
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
          :error="passwordError"
          :error-messages="passwordErrorMessages"
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
      usernameError: false,
      usernameErrorMessages: [],
      password: '',
      passwordRules: [
        v => !!v || 'Password is required'
      ],
      passwordError: false,
      passwordErrorMessages: [],
      loginMethod: 'local',
      loginMethods: [
        'local',
        'ldap'
      ],
      loginInProgress: false
    }
  },
  watch: {
    username () {
      this.usernameError = false
      this.usernameErrorMessages = this.passwordErrorMessages = []
    },
    password () {
      this.passwordError = false
      this.usernameErrorMessages = this.passwordErrorMessages = []
    }
  },
  methods: {
    login () {
      this.loginInProgress = true
      this.$store.dispatch('login', {
        username: this.username,
        password: this.password,
        method: this.loginMethod,
        ignoreAPIError: true
      })
        .then((data) => {
          this.$emit('success')
          return data
        })
        .catch((data) => {
          this.usernameError = this.passwordError = true
          this.usernameErrorMessages = this.passwordErrorMessages = []
          if (data.message) {
            this.usernameErrorMessages = this.passwordErrorMessages = [data['message']]
          } else {
            this.usernameErrorMessages = this.passwordErrorMessages = ['Server didn\'t response in a expected way']
          }
          return data
        })
        .then((res) => {
          this.loginInProgress = false
          return res
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
