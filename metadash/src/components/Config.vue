<template>
  <div class="container">
    <div v-if="loaded">
      <div v-for="value in plugins" class="panel panel-default">
        <div class="panel-heading">
          <h1 class="panel-title">{{ value.plugin }}</h1>
        </div>
        <div class="panel-body">
          <form class="form-horizontal">
            <div v-for="config in value.configs" :key="config.key" class="form-group" v-bind:class="{ 'has-error': config.error }">
              <label class="col-sm-2 control-label" for="textInput-markup">{{ config.key }}</label>
              <div class="col-sm-10">
                <input type="text" id="textInput-markup" class="form-control" v-model="config.value">
                <span class="help-block">{{ config.description }}</span>
                <span v-if="config.error" class="help-block">{{ config.error }}</span>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div v-else>
      <h1> Loading ... </h1>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
export default {
  name: 'config',
  data () {
    return {
      'loaded': false,
      'savedConfigs': [],
      'oldConfigs': [],
      'configs': []
    }
  },
  mounted () {
    this.load()
  },
  methods: {
    save: _.debounce(function () {
      let changedConfigs = _.differenceBy(this.configs, this.savedConfigs, 'value')
      changedConfigs.map((config) => {
        if (config.error) {
          return
        }
        this.$http.put('/api/configs/' + config.key, {
          value: config.value
        }).then((res) => {
          this.debouncedLoad()
        }, (errRes) => {
          config.error = 'Failed to save'
        })
      })
    }, 500),
    load () {
      this.$http.get('/api/configs').then((res) => {
        res.json().then((data) => {
          this.savedConfigs = JSON.parse(JSON.stringify(data.data))
          this.configs = data.data
          this.loaded = true
        })
      })
    },
    debouncedLoad: _.debounce(function () {
      this.load()
    }, 500)
  },
  watch: {
    configs: {
      handler (newConfig) {
        let changedConfigs = _.differenceBy(newConfig, this.oldConfigs, 'value')
        for (let config of changedConfigs) {
          if (!config.nullable && !config.value) {
            config.error = "Can't be empty"
          } else {
            config.error = false
          }
        }
        this.oldConfigs = JSON.parse(JSON.stringify(newConfig))
        this.save()
      },
      deep: true
    }
  },
  computed: {
    plugins () {
      // Sort configs by plugin name
      return this.configs.reduce(
      (plugins, curConfig) => {
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
