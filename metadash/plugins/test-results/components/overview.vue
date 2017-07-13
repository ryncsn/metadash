<template>
  <div class="container">
    <pf-toolbar :filter-fields="filterFields" views="table,card" :filters="filters">
      <bs-dropdown v-for="values, prop in filterProperties" :text="prop" :key="prop">
        <li v-for="v in values" :key="v"><a @click="applyFilter(prop, v)" href="#">{{ v }}</a></li>
      </bs-dropdown>
    </pf-toolbar>
    <transition-group tag="div" name="testrun-list">
      <testrun-card v-for="testrun in testruns" :testrun="testrun" :key="testrun.uuid" class="testrun-list-item">
      </testrun-card>
    </transition-group>
  </div>
</template>

<script>
import TestrunCard from './testrun-card.vue'
import _ from 'lodash'
export default {
  components: {TestrunCard},
  data () {
    return {
      testruns: [],
      filterProperties: {},
      filterTags: [],
      filterName: '',
      filterTestCaseName: '',
      filters: [],
      avaliableFilters: []
    }
  },
  methods: {
    refresh () {
      this.$http.get('/api/testruns?' + this.filters.map(f => `${f.name}=${f.value}`).join('&'))
        .then(res => res.json())
        .then(data => {
          this.testruns = data.data
          this.filterProperties = data.filter_properties
          this.filterTags = data.filter_tags
        })
    },
    applyFilter (key, value) {
      let applied = _.find(this.filters, {name: key})
      if (applied) {
        applied.value = value
      } else {
        this.filters.push({
          'label': _.upperFirst(key),
          'name': key,
          'value': value
        })
      }
    },
    changePage (page) {
      this.page = page
    }
  },
  mounted () {
    this.refresh()
  },
  computed: {
    filterFields () {
      return Array.concat(['name'], this.avaliableFilters)
    }
  },
  watch: {
    filters: {
      handler () {
        this.refresh()
      },
      deep: true
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.testrun-list-item {
  transition: all 0.5s;
}
.testrun-list-enter-active {
  opacity: 0;
}
.testrun-list-leave-active {
  opacity: 0;
  height: 0;
  margin-top: 0;
  margin-bottom: 0;
  padding-top: 0;
  padding-bottom: 0;
  border-top-width: 0;
  border-bottom-width: 0;
  float: right;
}
</style>
