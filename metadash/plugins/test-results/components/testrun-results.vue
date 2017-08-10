<template>
  <div>
    <div v-if="failed.length">
      <h2> Failed Test Cases: </h2>
      <ul class="list-group">
        <router-link tag="a" v-for="result in failed" :key="result.testcase_name" :to="{ path: `/test-results/testresult/${result.uuid}` }" class="list-group-item">
          {{result.testcase_name}}
        </router-link>
      </ul>
      <hr>
    </div>
    <div v-if="skipped.length">
      <h2> Skipped Test Cases: </h2>
      <ul class="list-group">
        <router-link tag="a" v-for="result in skipped" :key="result.testcase_name" :to="{ path: `/test-results/testresult/${result.uuid}` }" class="list-group-item">
          {{result.testcase_name}}
        </router-link>
      </ul>
      <hr>
    </div>
    <div v-if="passed.length">
      <h2> All Test Cases: </h2>
      <ul class="list-group">
        <router-link tag="a" v-for="result in results" :key="result.testcase_name" :to="{ path: `/test-results/testresult/${result.uuid}` }" class="list-group-item">
          {{result.testcase_name}}
        </router-link>
      </ul>
      <hr>
    </div>
  </div>
</template>

<script>
export default {
  props: ['results'],
  data () {
    return {}
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
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
