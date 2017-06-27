<template>
  <form class="form-horizontal">
    <div class="form-group" :class="{ 'has-error': error }">
      <label class="col-sm-2 control-label" for="textInput-markup">Username</label>
      <div class="col-sm-10">
        <input type="text" id="textInput-markup" class="form-control" v-model="username" @keyup.enter="login">
      </div>
    </div>
    <div class="form-group" :class="{ 'has-error': error }">
      <label class="col-sm-2 control-label" for="inputError-markup">Password</label>
      <div class="col-sm-10">
        <input type="password" id="inputError-markup" class="form-control" v-model="password" @keyup.enter="login">
        <span v-if="error" class="help-block">{{ error }}</span>
      </div>
    </div>
    <button class="btn btn-primary btn-lg" :class="{'disabled': loginInProgress}" type="button" @click="login">Login</button>
  </form>
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
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div {
  text-align: center;
}

button {
  margin-left: auto;
  margin-right: auto;
}
</style>
