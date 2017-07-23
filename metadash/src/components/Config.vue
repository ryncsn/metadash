<template>
  <div class="container">
    <div class="panel panel-default">
      <div class="panel-heading">
        <h1 class="panel-title"> User & permissions </h1>
      </div>
      <div class="panel-body">
        <md-permission>
        </md-permission>
      </div>
    </div>
    <div v-for="value in plugins" class="panel panel-default">
      <div class="panel-heading">
        <h1 class="panel-title">{{ value.plugin }}</h1>
      </div>
      <div class="panel-body">
        <form class="form-horizontal">
          <div v-for="config in value.configs" :key="config.key" class="form-group" v-bind:class="{ 'has-error': config.error }">
            <label class="col-sm-2 control-label" for="textInput-markup">{{ config.key }}</label>
            <div class="col-sm-10">
              <input type="text" id="textInput-markup" class="form-control" :value="config.value" @input="(event) => updateConfig(config.key, event)">
              <span class="help-block">{{ config.description }}</span>
              <span v-if="config.error" class="help-block">{{ config.error }}</span>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import MdPermission from '@/components/Permission'
export default {
  components: { MdPermission },
  name: 'md-config',
  data () {
    return {}
  },
  methods: {
    updateConfig (key, event) {
      this.$store.dispatch('updateConfig', {key, value: event.target.value})
    }
  },
  computed: {
    configs () {
      return this.$store.state.configs
    },
    plugins () {
      // Sort configs by plugin name
      return this.configs.reduce((plugins, curConfig) => {
        let plugin = plugins[curConfig.plugin] = plugins[curConfig.plugin] || {
          plugin: curConfig.plugin,
          configs: []
        }
        plugin.configs.push(curConfig)
        return plugins
      }, {})
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
