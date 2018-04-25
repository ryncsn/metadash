<template>
  <v-flex>
    <template v-for="item in alerts">
      <v-alert
       v-if="item.type !== 'info'"
       :type="item.type"
       dismissible
       transition="scale-transition"
       v-model="item.alert">
      {{ item.msg }}
      </v-alert>
      <v-snackbar
        v-else
        timeout=6000
        top
        right
        color="green"
        v-model="item.alert"
      >
        <v-icon>check_circle</v-icon>
        {{ item.msg }}
        <v-btn flat @click.native="item.alert = false">
          <v-icon>close</v-icon>
        </v-btn>
      </v-snackbar>
    </template>
  </v-flex>
</template>

<script>
export default {
  name: 'alert',
  computed: {
    alerts () {
      return this.$store.state.alerts
    }
  }
}
</script>

<style scoped>
</style>
