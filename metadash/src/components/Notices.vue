<template>
  <v-list>
    <v-list-group>
      <v-list-tile slot="activator">
        <v-list-tile-content>
          <v-list-tile-title>Recent Activities</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
      <v-list-tile>
        <v-list-tile-content>
          <v-list-tile-title>User xxx triggerd jobs</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list-group>
    <v-list-group>
      <v-list-tile slot="activator">
        <v-list-tile-content>
          <v-list-tile-title>Alerts</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
      <v-list-tile v-for="(item, index) in alerts" :key="`alert-${index}`">
        <v-list-tile-content>
          <v-list-tile-title>{{ item.msg }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list-group>
    <tasks/>
    <v-list-group>
      <v-list-tile slot="activator">
        <v-list-tile-content>
          <v-list-tile-title>Server Info</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
      <v-list-tile>
        <v-list-tile-content>
          <v-list-tile-title>{{ metadashVersion }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list-group>
  </v-list>
</template>

<script>
import Tasks from './Tasks.vue'
export default {
  props: [ 'metadashVersion' ],
  components: { Tasks },
  data () {
    return {
      activities: []
    }
  },
  computed: {
    alerts () {
      return this.$store.state.alerts
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
