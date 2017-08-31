<template>
  <pf-card :title="title" :foot-note="footer" foot-icon="fa fa-tags" :class="{'card-loading': !finished}">
    <i class="fa title-icon" :class="titleIcon"></i>
    <a :href="ref_url" target="_blank" v-if="ref_url"><i class="fa fa-link" aria-hidden="true"></i> Testrun Page</a>
    <span class="test-summary pull-right" v-if="finished">
      <a href="#"><span class="pficon pficon-error-circle-o"></span> {{failed}} </a>
    </span>
    <span class="test-summary pull-right" v-if="finished">
      <a href="#"><span class="pficon pficon-warning-triangle-o"></span> {{skipped}} </a>
    </span>
    <span class="test-summary pull-right" v-if="finished">
      <a href="#"><span class="pficon pficon-ok"></span> {{passed}} </a>
    </span>
    <router-link :to="{ path: '/test-results/testrun/' + uuid + '/' }"
      tag="a" class="btn btn-primary pull-right" type="button">Details</router-link>
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
    titleIcon () {
      if (!this.finished) {
        return {'fa-hourglass': true}
      } else if (!this.failed) {
        return {'fa-check': true}
      } else {
        return {'fa-bug': true}
      }
    },
    finished () {
      return this.testrun.status !== 'PENDING'
    },
    status () {
      return this.testrun.status
    },
    title () {
      return this.testrun.name || 'N/a'
    },
    footer () {
      return (this.testrun.tags.join(' ') || 'No Tag') + `    Executed at: ${this.testrun.timestamp}`
    },
    ref_url () {
      return this.testrun.ref_url || '#'
    },
    uuid () {
      return this.testrun.uuid
    },
    passed () {
      return this.testrun.results.PASSED || 0
    },
    failed () {
      return this.testrun.results.FAILED || 0
    },
    skipped () {
      return this.testrun.results.SKIPPED || 0
    }
  },
  created () {
  },
  watch: {
  }
}
</script>

<style>
.title-icon {
  font-size: 24px;
  margin-right: 30px;
  border-right: 1px solid #d1d1d1;
  padding-right: 10px;

}
.test-summary {
  color: #363636;
  line-height: 1;
  font-size: 24px;
  font-weight: 300;
  margin-left: 30px;
  border-left: 1px solid #d1d1d1;
  padding-left: 10px;
}

.card-loading {
  background-color: #eee;
  background-size: 40px 40px;
  background-image: -webkit-linear-gradient(
    -45deg,
    rgba(255, 255, 255, .2) 25%,
    transparent 25%,
    transparent 50%,
    rgba(255, 255, 255, .2) 50%,
    rgba(255, 255, 255, .2) 75%,
    transparent 75%,
    transparent
  );
}
</style>
