<template>
  <div v-if="data">
    <h1> <router-link tag="a" :to="{ path: `/test-results/testrun/${data.testrun_uuid}/` }" class="back-button"><i class="fa fa-angle-left" aria-hidden="true"></i></router-link> Test Result </h1> <hr>
    <h1> {{data.testcase_name}} <span class="label" :class="resultLabel"> {{data.result}} </span> </h1> <hr>

    <h4> Duration: {{data.duration}} @ {{data.timestamp}} <a :href="data.ref_url" target="_blank">Ref</a> </h4>

    <table class="table">
      <thead>
        <tr><td>Property</td><td>Value</td></tr>
      </thead>
      <tbody>
        <tr v-for="value, key in data.properties"><td> {{key}} </td> <td> {{value}} </td> </tr>
      </tbody>
    </table>

    <div v-for="value, key in data.details">
      <h2> {{key}} </h2>
      <pre> {{value || '--Empty--' }} </pre>
    </div>
  </div>
</template>

<script>
export default {
  props: ['uuid'],
  data () {
    return {
      data: null
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    refresh () {
      this.$http.get(`/api/testresults/${this.uuid}`)
        .then(res => res.json())
        .then(data => {
          this.data = data
        })
    }
  },
  watch: {
    uuid () { this.refresh() }
  },
  computed: {
    resultLabel () {
      if (this.data.result === 'PASSED') {
        return 'label-success'
      }
      if (this.data.result === 'FAILED') {
        return 'label-danger'
      }
      return 'label-warning'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.back-button {
  padding-left: 10px;
  padding-right: 15px;
  margin-right: 10px;
  border-right: 1px solid #d1d1d1;
}
</style>
