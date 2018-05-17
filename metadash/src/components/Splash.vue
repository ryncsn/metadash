<template>
  <v-jumbotron color="grey lighten-2" height="100%">
    <v-container fill-height>
      <v-layout align-center>
        <v-flex>
          <h3 class="display-1">Metadash is loading...</h3>
          <v-divider class="my-3"></v-divider>
          <div class="error-message-box" v-if="hasAlerts">Ooch, following error(s) occured:
            <br></br>
            <div v-for="alert in alerts">
              <span>
                {{alert}}
              </span>
              <br></br>
            </div>
          </div>
          <div v-else class="title mb-3">Please wait, this won't take long...</div>
        </v-flex>
      </v-layout>
    </v-container>
  </v-jumbotron>
</template>

<script>
export default {
  name: 'loading-splash',
  data () {
    return {
    }
  },
  computed: {
    alerts () {
      return this.$store.state.alerts
    },
    hasAlerts () {
      return this.$store.state.alerts.length !== 0
    }
  }
}
</script>

<style scoped>
.error-message-box {
  color: red;
}
</style>

