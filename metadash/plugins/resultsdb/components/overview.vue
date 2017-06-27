<template>
  <div>
    <pf-toolbar :filter-fields="filterFields" @filters="applyFilters">
    </pf-toolbar>
    <pf-table :columns="['Testcase', 'Outcome', 'Data', 'Note', 'Submit Time', 'Link']" :rows="results" :page="page" :pages="pages" @change-page="changePage">
      <template scope="props">
        <td> {{ props.row.testcase.name }} </td>
        <td> {{ props.row.outcome }} </td>
        <td class="trapped"> <span class="label label-primary" style="margin-right: 5px;" v-for="(value, key) in props.row.data"> {{ key + ":" + value.join(", ") }} </span></td>
        <td> {{ props.row.note }} </td>
        <td> {{ props.row.submit_time }} </td>
        <td> <a :href="props.row.ref_url"> Ref </a> </td>
      </template>
      <slot name="action">
        action
      </slot>
      <slot name="dropdown">
        dropdown
      </slot>
    </pf-table>
  </div>
</template>

<script>
export default {
  data () {
    return {
      name: 'resultsdb-testresults',
      page: 1,
      sortable: true,
      results: [],
      filterFields: ['Loading'],
      filters: []
    }
  },
  methods: {
    refresh () {
      let appliedFilter = ''
      for (let filter of this.filters) {
        if (filter.value.indexOf('*') !== -1) {
          appliedFilter += `${filter.name}:like=${filter.value}`
        } else {
          appliedFilter += `${filter.name}=${filter.value}`
        }
      }
      this.$http.get(`/api/results?page=${this.page}&${appliedFilter}`)
        .then(res => res.json())
        .then(data => {
          let availablefilters = new Set()
          for (let res of data.data) {
            for (let property of Object.keys(res.data)) {
              availablefilters.add(property)
            }
          }
          this.filterFields = Array.from(availablefilters)
          this.results = data.data
        })
    },
    changePage (page) {
      this.page = page
    },
    applyFilters (filters) {
      this.filters = filters
    }
  },
  mounted () {
    this.refresh()
  },
  computed: {
    pages () {
      return this.page + 10
    }
  },
  watch: {
    page () {
      this.refresh()
    },
    filters () {
      this.refresh()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.trapped {
  overflow: scroll;
  overflow-y: hidden;
  max-width: 400px;
}
</style>
