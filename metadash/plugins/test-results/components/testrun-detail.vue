<template>
  <div>
    <h1> <router-link tag="a" :to="{ path: '/test-results/' }" class="back-button"><i class="fa fa-angle-left" aria-hidden="true"></i></router-link> Test Run </h1>
    <hr>
    <h1> {{ data.name || 'Loading...' }} </h1>
    <h3> Results: {{ passed.length + " passed, " + failed.length + " failed, " + skipped.length + " skipped. " }} </h3>
    <hr>
    <ul class="nav nav-tabs">
      <router-link tag="li" active-class="active" to="results"><a>Results</a></router-link>
      <router-link tag="li" active-class="active" to="parameters"><a>Parameter</a></router-link>
      <router-link tag="li" active-class="active" to="details"><a>Details</a></router-link>
      <router-link tag="li" active-class="active" to="short-cuts"><a>Short Cuts</a></router-link>
    </ul>
    <router-view :testrun="data" :results="results"></router-view>
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
      if (!this.uuid) {
        return
      }
      this.data = {}
      this.results = []
      this.$http.get('/api/testruns/' + this.uuid)
        .then(res => res.json())
        .then(data => {
          this.data = data
        }).then(() => {
          this.$http.get('/api/testresults/?testrun_uuid=' + this.uuid + '&limit=0')
            .then(res => res.json())
            .then(data => {
              this.results = data.data
            })
        })
    }
  },
  watch: {
    uuid () { this.refresh() }
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
