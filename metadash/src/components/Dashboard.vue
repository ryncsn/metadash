<template>
  <v-card flat height="100%" :img="backImgUrl" class="backimg">
    <v-menu
      v-model="menu"
      :close-on-content-click="false"
      :nudge-width="200"
      nudge-left="330px"
      offset-x
    >
      <v-btn fab right bottom color="teal lighten-2" slot="activator" dark fixed>
        <v-icon>dashboard</v-icon>
      </v-btn>
      <v-list>
        <v-subheader>Saved dashboards</v-subheader>
        <v-divider/>
        <draggable :list="savedBoards" class="dragAreaSmall" @start="drag=true" @end="drag=false" :options="{group:'board'}" :move="onMoveCallback">
          <v-list-tile v-for="dashboard in savedBoards" :key="dashboard.name">
            <v-card flat>{{ dashboard.name }}</v-card>
          </v-list-tile>
          <v-card flat v-show="drag">
            <v-container fluid fill-height>
              <v-layout justify-center align-center>
                <v-flex text-xs-center>
                  <v-icon>add</v-icon>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
        </draggable>
      </v-list>
    </v-menu>
    <v-btn v-show="drag" fab right bottom color="blue" dark fixed>
      <draggable :list="savedBoards" class="dragAreaSmall" @start="drag=true" @end="drag=false" :options="{group:'board'}" :move="onMoveCallback">
        <v-icon>delete</v-icon>
      </draggable>
    </v-btn>
    <v-container fluid grid-list-lg>
      <v-layout row wrap>
        <v-flex v-for="(upboards, key) in topBoards" d-flex xs12 sm6 md3 :key="key">
          <v-card height="200px" flat :color="cardColor">
            <draggable :list="upboards" class="uponDragArea" row wrap @start="drag=true" :options="{group:'board'}" @end="drag=false" :move="onMoveCallback">
              <v-flex v-for="dashboard in upboards" :key="dashboard.name">
                <v-card>
                  <component v-bind:is="dashboard.module"></component>
                </v-card>
              </v-flex>
              <v-card-text v-show="drag">
                <v-container style="height: 200px;" fluid fill-height>
                  <v-layout justify-center align-center>
                    <v-flex text-xs-center>
                      <v-icon x-large>add</v-icon>
                    </v-flex>
                  </v-layout>
                </v-container>
              </v-card-text>
            </draggable>
          </v-card>
        </v-flex>
        <v-flex d-flex xs12 sm6 md8>
          <v-card flat :color="cardColor">
            <draggable :list="lgBoards" class="dragArea" row wrap @start="drag=true" :options="{group:'board'}" @end="drag=false" :move="onMoveCallback">
              <v-flex v-for="dashboard in lgBoards" :key="dashboard.name">
                <v-card>
                  <component v-bind:is="dashboard.module"></component>
                </v-card>
              </v-flex>
              <v-card-text v-show="drag">
                <v-container style="height: 480px;" fluid fill-height>
                  <v-layout justify-center align-center>
                    <v-flex text-xs-center>
                      <v-icon x-large>add</v-icon>
                    </v-flex>
                  </v-layout>
                </v-container>
              </v-card-text>
            </draggable>
          </v-card>
        </v-flex>
        <v-flex d-flex xs12 sm6 md4>
          <v-card flat :color="cardColor">
            <draggable :list="medBoards" class="dragArea" row wrap @start="drag=true" :options="{group:'board'}" @end="drag=false" :move="onMoveCallback">
              <v-flex v-for="dashboard in medBoards" :key="dashboard.name">
                <v-card>
                  <component v-bind:is="dashboard.module"></component>
                </v-card>
              </v-flex>
              <v-card-text v-show="drag">
                <v-container style="height: 480px;" fluid fill-height>
                  <v-layout justify-center align-center>
                    <v-flex text-xs-center>
                      <v-icon x-large>add</v-icon>
                    </v-flex>
                  </v-layout>
                </v-container>
              </v-card-text>
            </draggable>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-card>
</template>

<script>
import draggable from 'vuedraggable'
import { Plugins } from '@/plugin'
export default {
  name: 'dashboard',
  components: { draggable },
  data () {
    return {
      menu: false,
      fab: false,
      drag: false,
      backImgUrl: '',
      topBoards: {
        'topBoard0': [],
        'topBoard1': [],
        'topBoard2': [],
        'topBoard3': []
      },
      savedBoards: [],
      lgBoards: [],
      medBoards: []
    }
  },
  methods: {
    closePlugin (dashboard) {
      const index = this.dashboards.indexOf(dashboard)
      this.dashboards.splice(index, 1)
    },
    onMoveCallback (data, event) {
      if (data.to.className === 'uponDragArea' && data.relatedContext.list.length > 0) {
        return false
      }
    }
  },
  mounted () {
    let data = this.$store.getters.getConfig('BACKGROUND_IMG_URL')
    if (data) {
      this.backImgUrl = data.value
    }
    let defaultDashboard = {
    }
    for (let key in Plugins) {
      let plugin = Plugins[key]
      if (plugin.dashboard) {
        for (let subKey in plugin.dashboard) {
          let subDashboard = {
            'module': plugin.dashboard[subKey].component,
            'title': plugin.title,
            'path': plugin.path,
            'name': plugin.dashboard[subKey].name
          }
          if (subDashboard.name in defaultDashboard) {
            defaultDashboard[subDashboard.name].push(subDashboard)
          } else {
            this.savedBoards.push(subDashboard)
          }
        }
      }
    }
  },
  computed: {
    cardColor () {
      return this.drag ? 'grey' : 'transparent'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.backimg {
   min-height: 800px;
}
</style>
