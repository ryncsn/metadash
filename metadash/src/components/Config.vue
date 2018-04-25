<template>
  <v-container>
    <md-permission/>
    <v-card v-for="value in plugins" :key="value.plugin">
      <v-card-title>
        <v-toolbar color="pink">
          <v-toolbar-side-icon></v-toolbar-side-icon>
          <v-toolbar-title class="white--text">{{ value.plugin }}</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-card-text>
          <v-text-field
            v-for="config in value.configs"
            :label="config.description"
            :rules="[ check_error(config) ]"
            :key="`text-${value.plugin}-${config.key}`"
            :value="config.value"
            @input.native="(event) => updateConfig(config.key, event)"
          ></v-text-field>
        </v-card-text>
      </v-card-title>
    </v-card>
  </v-container>
</template>

<script>
import MdPermission from '@/components/Permission'
export default {
  components: { MdPermission },
  name: 'md-config',
  data () {
    return {
    }
  },
  methods: {
    updateConfig (key, event) {
      this.$store.dispatch('updateConfig', {key, value: event.target.value})
    },
    check_error (config) {
      return config.error || true
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
