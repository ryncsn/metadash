<template>
  <pf-card :title="title" :foot-note="footer" foot-icon="fa fa-tags">
    <div clss="pull-right">
      <a :href="ref_url" target="_blank">Testrun Page</a>
      <span class="test-summary pull-right">
        <a href="#"><span class="pficon pficon-error-circle-o"></span> {{error}} </a>
      </span>
      <span class="test-summary pull-right">
        <a href="#"><span class="pficon pficon-warning-triangle-o"></span> {{skipped}} </a>
      </span>
      <span class="test-summary pull-right">
        <a href="#"><span class="pficon pficon-ok"></span> {{passed}} </a>
      </span>
      <router-link :to="{ path: '/test-results/testrun/' + uuid }"
        tag="button" class="btn btn-primary pull-right" type="button">Details</router-link>
    </div>
  </pf-card>
</template>

<script>
import Dropdown from 'vue-strap/src/Dropdown'
export default {
  name: 'job-card',
  components: { Dropdown },
  props: [ 'testrun' ],
  data () {
    return {}
  },
  methods: {
  },
  computed: {
    title () {
      return this.testrun.name || 'N/a'
    },
    footer () {
      return this.testrun.tags.join(' ') || 'No Tag'
    },
    ref_url () {
      return this.testrun.ref_url || '#'
    },
    uuid () {
      return this.testrun.uuid
    }
  },
  created () {
  },
  watch: {
  }
}
</script>

<style scoped>
.test-summary {
  color: #363636;
  line-height: 1;
  font-size: 24px;
  font-weight: 300;
  margin-left: 30px;
  border-left: 1px solid #d1d1d1;
  padding-left: 10px;
}
</style>
