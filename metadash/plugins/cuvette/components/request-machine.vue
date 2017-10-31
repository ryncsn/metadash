<template>
  <div>
    <div v-if="parameterMeta != null">
      <form class="form-horizontal" role="form">
        <div class="form-group" :v-class="{'has-error': value.error }" v-for="(value, key) in parameterMeta" :key="key">
          <label class="col-sm-2 control-label" for="textInput-markup">{{ key }}</label>
          <div class="col-sm-10">
            <input type="text" id="textInput-markup" :v-model="parameters[key]" class="form-control">
            <span class="help-block">{{ value }}</span>
          </div>
        </div>
        <div class="form-group">
          <label class="col-sm-2 control-label" for="textInput-markup">Default</label>
          <div class="col-sm-10">
            <input type="text" id="textInput-markup" class="form-control">
          </div>
        </div>
        <div class="form-group">
          <label class="col-sm-2 control-label" for="textInputDisabled-markup">Disabled</label>
          <div class="col-sm-10">
            <input type="text" id="textInputDisabled-markup" class="form-control" disabled>
          </div>
        </div>
        <div class="form-group has-error">
          <label class="col-sm-2 control-label" for="inputError-markup">With error</label>
          <div class="col-sm-10">
            <input type="text" id="inputError-markup" class="form-control">
            <span class="help-block">Please correct the error</span>
          </div>
        </div>
      </form>
    </div>
    <div v-else>
      <h1> Loading Paremeters... </h1>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      parameterMeta: {},
      parameters: {}
    }
  },
  methods: {
    refresh () {
      this.$http.get('/api/cuvette-machine-parameters')
        .then(res => res.json())
        .then(data => {
          this.parameterMeta = data
          console.log(this.parameterMeta)
        })
    },
    validate () {
    }
  },
  mounted () {
    this.refresh()
  },
  watch: {
    parameters () {
      console.log(this.parameter)
    }
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div {
  text-align: center;
}

h1, h2 {
  font-weight: normal;
}
</style>
