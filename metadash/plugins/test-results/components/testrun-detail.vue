<template>
  <div>
    <h1>
      <router-link tag="a" :to="{ path: '/test-results/' }" class="back-button"><i class="fa fa-angle-left" aria-hidden="true"></i></router-link> Test Run
    </h1>
    <hr>
    <div class="jumbotron" :style=" {'background-color': backgroundColor} ">
      <h1> {{ data.name || 'Loading...' }} </h1>
      <h3> {{ passed + " passed, " + failed + " failed, " + skipped + " skipped. " }} </h3>
    </div>
  </div>
</template>

<script>
export default {
  name: 'test-run',
  props: ['uuid'],
  data () {
    return {
      data: {
      }
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
        })
    }
  },
  computed: {
    passed () {
      return this.data.results.PASSED || 'N/a'
    },
    failed () {
      return this.data.results.FAILED || 'N/a'
    },
    skipped () {
      return this.data.results.SKIPPED || 'N/a'
    },
    backgroundColor () {
      if (this.data.results) {
        if (this.failed) {
          return '#FFDBD8'
        } else if (this.skipped) {
          return '#F9E79F'
        } else if (this.passed) {
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
