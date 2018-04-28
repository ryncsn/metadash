<template>
  <v-list-group>
    <v-list-tile slot="activator">
      <v-list-tile-content>
        <v-list-tile-title>Running tasks</v-list-tile-title>
      </v-list-tile-content>
    </v-list-tile>
    <v-list-tile
      v-if="tasks.length == 0"
    >
      <v-list-tile-content>
        <v-list-tile-title>No Task running</v-list-tile-title>
      </v-list-tile-content>
    </v-list-tile>
    <template v-for="task in tasks">
      <v-list-tile
        :key="task.name"
      >
        <v-list-tile-action>
          <v-progress-circular color="primary" :value="task.meta"></v-progress-circular>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>{{task.name}}</v-list-tile-title>
          <v-spacer/>
          <v-list-tile-sub-title>{{task.state}}</v-list-tile-sub-title>
        </v-list-tile-content>
      </v-list-tile>
    </template>
  </v-list-group>
</template>
<script>
import _ from 'lodash'
export default {
  name: 'md-permission',
  data () {
    return {
      'tasks': []
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    refresh () {
      return this.$http.get('/api/tasks')
        .then(res => res.json())
        .then(data => {
          this.tasks = data
        })
    }
  },
  computed: {
    columns () {
      return ['User'].concat(this.roles.map(_.upperFirst))
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
