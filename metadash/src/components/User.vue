<template>
  <v-layout align-center justify-center>
    <v-flex>
      <v-card>
        <v-card-title class="headline">Do you really want to log out?</v-card-title>
        <v-card-text>You will logout with user: {{ username || "Not Login" }} role: {{ role }}</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" flat @click="logout" :disabled="logoutInProgress">Yes</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
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
