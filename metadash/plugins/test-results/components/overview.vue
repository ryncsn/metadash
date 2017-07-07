<template>
  <div class="container">
    <pf-toolbar :filter-fields="filterFields" views="table,card">
    </pf-toolbar>
    <testrun-card v-for="testrun in testruns" :testrun="testrun">
    </testrun-card>
  </div>
</template>

<script>
import TestrunCard from './testrun-card.vue'
export default {
  components: {TestrunCard},
  data () {
    return {
      testruns: [],
      filterProperties: [],
      filterTags: [],
      filterName: '',
      avaliableFilters: []
    }
  },
  methods: {
    refresh () {
      this.$http.get('/api/testruns')
        .then(res => res.json())
        .then(data => {
          this.testruns = data.data
        })
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
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
