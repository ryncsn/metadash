<template>
  <div>
    <div v-if="tasks.length == 0">
      <div class="task-panel">
        No Task running
      </div>
    </div>
    <div class="task-panel" v-for="task in tasks">
      <div class="progress-description">
        <div class="spinner spinner-xs spinner-inline"></div> <strong>{{task.name}}</strong>
      </div>
      <div class="progress progress-label-top-right">
        <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar"
          style="width: 100%" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">
          {{task.meta}}
          <span>{{task.state}}</span>
        </div>
      </div>
    </div>
  </div>
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
.task-panel {
  padding: 20px;
}
</style>
