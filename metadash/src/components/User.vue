<template>
  <div>
    <div class="card-pf card-pf-view">
      <div class="card-pf-body">
        <div class="card-pf-top-element">
          <span class="fa fa-user card-pf-icon-circle"></span>
        </div>
        <h2 class="card-pf-title text-center">
          {{ username || 'Not Logged In' }}
        </h2>
        <div class="card-pf-items text-center">
          {{ role }}
          <br>
          <br>
          <button v-if="username" class="btn btn-danger btn-lg" :class="{'disabled': logoutInProgress}" type="button" @click="logout">Logout</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'user',
  data () {
    return {
      logoutInProgress: false
    }
  },
  methods: {
    logout () {
      this.logoutInProgress = true
      this.$store.dispatch('logout')
        .then(() => {
          this.$emit('success')
        }, () => {
          this.$emit('failed')
        })
        .then(() => { this.logoutInProgress = false })
    }
  },
  computed: {
    username () {
      return this.$store.state.username
    },
    role () {
      return this.$store.state.role || 'anonymous'
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
