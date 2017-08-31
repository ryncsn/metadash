<template>
  <div>
    <pf-card :title="fullName" :show-titles-separator="false">
      <a :href="jenkinsUrl + '/job/' + provisionName" target="_blank">Jenkins Provision Page</a>
      <a :href="jenkinsUrl + '/job/' + runtestName" target="_blank">Jenkins Runtest Page</a>
      <a :href="jenkinsUrl + '/job/' + teardownName" target="_blank">Jenkins Teardown Page</a>
      <router-link tag="a" :to="`/test-results?arch=${arch}&component=${component}&product=${product}-${version}&`"><a>Results</a></router-link>
      <a class="pull-right" href="javascript:void(0)" @click="deleteJob">Delete from list</a>
    </pf-card>
  </div>
</template>

<script>
import Dropdown from 'vue-strap/src/Dropdown'
export default {
  name: 'job-card',
  components: { Dropdown },
  props: [ 'arch', 'product', 'version', 'component', 'jobName', 'jenkinsUrl', 'name' ],
  data () {
    return {}
  },
  methods: {
    deleteJob () {
      this.$emit('deleteJob')
    }
  },
  computed: {
    fullName () {
      return this.name
    },
    runtestName () {
      return `${this.component}-${this.product}-${this.version}-runtest-${this.arch}-${this.jobName}`
    },
    provisionName () {
      return `${this.component}-${this.product}-${this.version}-provision-${this.arch}-${this.jobName}`
    },
    teardownName () {
      return `${this.component}-${this.product}-${this.version}-teardown-${this.arch}-${this.jobName}`
    }
  },
  created () {
  },
  watch: {
  }
}
</script>

<style scoped>
a {
  margin-right: 12px;
}
</style>
