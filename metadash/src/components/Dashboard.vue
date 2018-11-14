<template>
  <v-container fluid grid-list-lg>
    <draggable element="v-layout" :list="dashboards" row wrap @start="drag=true" @end="drag=false">
      <v-flex xs6 v-for="dashboard in dashboards" :key="dashboard.title">
        <v-card>
          <v-speed-dial
            v-model="actionsFab"
            direction="left"
            absolute
            right
          >
            <v-btn
              slot="activator"
              color="transparent"
              small
              fab
              v-show=false
              v-model="actionsFab"
            >
              <v-icon>menu</v-icon>
            </v-btn>
            <v-tooltip bottom>
              <v-btn
                color="light-blue"
                slot="activator"
                dark
                small
                fab
                @click="closePlugin(dashboard)"
              >
                <v-icon>close</v-icon>
              </v-btn>
              <span>Close</span>
            </v-tooltip>
            <v-tooltip bottom>
              <v-btn
                color="light-blue"
                slot="activator"
                dark
                small
                fab
                :to="dashboard.path"
              >
                <v-icon>info</v-icon>
              </v-btn>
              <span>{{dashboard.title}}</span>
            </v-tooltip>
            <v-tooltip bottom>
              <v-btn
                color="light-blue"
                slot="activator"
                dark
                small
                fab
                :to="dashboard.path"
              >
                <v-icon>link</v-icon>
              </v-btn>
              <span>plugin page</span>
            </v-tooltip>
          </v-speed-dial>
          <component v-bind:is="dashboard.module"></component>
        </v-card>
      </v-flex>
    </draggable>
  </v-container>
</template>

<script>
import draggable from 'vuedraggable'
import { Plugins } from '@/plugin'
export default {
  name: 'hello',
  components: { draggable },
  data () {
    return {
      actionsFab: true,
      drag: false,
      dashboards: []
    }
  },
  methods: {
    closePlugin (dashboard) {
      const index = this.dashboards.indexOf(dashboard)
      this.dashboards.splice(index, 1)
    }
  },
  mounted () {
    for (let key in Plugins) {
      let plugin = Plugins[key]
      if (plugin.dashboard) {
        for (let subKey in plugin.dashboard) {
          let subDashboard = plugin.dashboard[subKey]
          this.dashboards.push({'module': subDashboard.component, 'title': plugin.title, 'path': plugin.path, 'name': subDashboard.name})
        }
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
