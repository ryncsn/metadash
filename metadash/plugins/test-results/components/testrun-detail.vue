<template>
  <div>
    <h1> <router-link tag="a" :to="{ path: '/test-results/' }" class="back-button"><i class="fa fa-angle-left" aria-hidden="true"></i></router-link> Test Run </h1>
    <hr>
    <h1> {{ data.name || 'Loading...' }} </h1>
    <h3> Results: {{ passed.length + " passed, " + failed.length + " failed, " + skipped.length + " skipped. " }} </h3>
    <hr>
    <ul class="nav nav-tabs">
      <li class="active"><a href="#">Properties</a></li>
      <li class="active"><a href="#">Details</a></li>
      <li><a href="#">Test Results</a></li>
      <li><a href="#">Short cuts</a></li>
    </ul>

    <table class="table">
      <thead>
        <tr><td>Property</td><td>Value</td></tr>
      </thead>
      <tbody>
        <tr v-for="value, key in data.properties"><td> {{key}} </td> <td> {{value}} </td> </tr>
      </tbody>
    </table>

    <table class="table">
      <thead>
        <tr><td>Detail</td><td>Value</td></tr>
      </thead>
      <tbody>
        <tr v-for="value, key in data.details"><td> {{key}} </td> <td> {{value}} </td> </tr>
      </tbody>
    </table>

    <div v-if="failed.length">
      <h2> Failed Test Cases: </h2>
      <ul class="list-group">
        <li v-for="result in failed" :key="result.testcase_name" class="list-group-item"> {{result.testcase_name}} </li>
      </ul>
      <hr>
    </div>
    <div v-if="skipped.length">
      <h2> Skipped Test Cases: </h2>
      <ul class="list-group">
        <router-link tag="a" v-for="result in skipped" :key="result.testcase_name" :to="{ path: `/test-results/testresult/${result.uuid}` }" class="list-group-item"> {{result.testcase_name}} </router-link>
      </ul>
      <hr>
    </div>
    <div v-if="passed.length">
      <h2> All Test Cases: </h2>
      <ul class="list-group">
        <router-link tag="a" v-for="result in results" :key="result.testcase_name" :to="{ path: `/test-results/testresult/${result.uuid}` }" class="list-group-item"> {{result.testcase_name}} </router-link>
      </ul>
      <hr>
    </div>
  </div>
</template>

<script>
export default {
  name: 'test-run',
  props: ['uuid'],
  data () {
    return {
      data: {},
      results: []
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    refresh () {
      this.$http.get('/api/testruns/' + this.uuid)
        .then(res => res.json())
        .then(data => {
          this.data = data
        }).then(() => {
          this.$http.get('/api/testresults/?testrun_uuid=' + this.uuid)
            .then(res => res.json())
            .then(data => {
              this.results = data.data
            })
        })
    }
  },
  computed: {
    passed () {
      return this.results.filter(r => r.result === 'PASSED')
    },
    failed () {
      return this.results.filter(r => r.result === 'FAILED')
    },
    skipped () {
      return this.results.filter(r => r.result === 'SKIPPED')
    },
    backgroundColor () {
      if (this.results) {
        if (this.failed.length) {
          return '#FFDBD8'
        } else if (this.skipped.length) {
          return '#F9E79F'
        } else if (this.passed.length) {
          return '#D5F5E3'
        }
      }
      return '#d1d1d1'
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
