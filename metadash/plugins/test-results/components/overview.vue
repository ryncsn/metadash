<template>
  <div class="container">
    <pf-toolbar :filter-fields="filterFields" views="table,card" :filters="filters" :result-count="total">
      <bs-dropdown v-for="values, prop in filterProperties" :text="prop" :key="prop">
        <li v-for="v in values" :key="v"><a @click="applyFilter(prop, v)" href="#">{{ v }}</a></li>
      </bs-dropdown>
    </pf-toolbar>
    <horizon-loader :loading="loading"></horizon-loader>
    <transition-group tag="div" name="testrun-list">
      <testrun-card v-for="testrun in testruns" :testrun="testrun" :key="testrun.uuid" class="testrun-list-item">
      </testrun-card>
    </transition-group>
    <pf-paginate-control :page="page" :pages="pages" @change="setPage">
    </pf-paginate-control>
  </div>
</template>

<script>
import TestrunCard from './shared/testrun-card.vue'
import HorizonLoader from '@/components/HorizonLoader'
import _ from 'lodash'

export default {
  components: {TestrunCard, HorizonLoader},
  props: {
    filtersArg: {
      default: () => [],
      type: Object.Array
    },
    test: {
      default: null
    }
  },
  data () {
    return {
      loading: false,
      testruns: [],

      // Filtering Info
      filterProperties: {},
      filterTags: [],
      // filterName: '',
      // filterTestCaseName: '',
      filters: [],
      avaliableFilters: [], // Not used yet

      // Paging info
      limit: 30,
      total: 30,
      page: 1
    }
  },
  methods: {
    refresh () {
      this.loading = true
      this.$router.replace({query: this.filters.reduce((sum, f) => { sum[[f.name]] = f.value; return sum }, {})})
      this.$http.get(`/api/testruns?page=${this.page}&limit=${this.limit}&` + this.filters.map(f => `${f.name}=${f.value}`).join('&'))
        .then(res => res.json())
        .then(data => {
          this.testruns = data.data
          this.filterProperties = data.filter_properties
          this.filterTags = data.filter_tags
          this.total = data.total
          this.loading = false
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
    setPage (page) {
      this.page = page
    }
  },
  mounted () {
    this.filters = this.filtersArg
    this.refresh()
  },
  computed: {
    filterFields () {
      return Array.concat(['name'], this.avaliableFilters)
    },
    pages () {  // caculate how many pages avaliable by limit and totalCount
      return _.ceil(this.total / this.limit)
    }
  },
  watch: {
    filters: {
      handler () { this.refresh() },
      deep: true
    },
    page () { this.refresh() }
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
