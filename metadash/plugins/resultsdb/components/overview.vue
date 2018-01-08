<template>
  <div>
    <pf-toolbar :filter-fields="filterFields" :filters="filters">
    </pf-toolbar>
    <horizon-loader :loading="loading"></horizon-loader>
    <pf-table :columns="['Testcase', 'Outcome', 'Data', 'Note', 'Submit Time', 'Link']" :rows="results" :page="page" :pages="pages" @change-page="changePage">
      <template slot-scope="props">
        <td> {{ props.row.testcase.name }} </td>
        <td> {{ props.row.outcome }} </td>
        <td class="trapped">
          <a class="label label-primary" style="margin-right: 5px;" v-for="(value, key) in props.row.data" @click="applyFilter(key, value[0])">
            {{ key + ":" + value.join(", ") }} </a>
        </td>
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
import HorizonLoader from '@/components/HorizonLoader'
export default {
  components: { HorizonLoader },
  data () {
    return {
      loading: false,
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
      this.loading = true
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
          this.loading = false
        })
    },
    changePage (page) {
      this.page = page
    },
    applyFilter (key, value) {
      this.filters.push({
        label: key,
        name: key,
        value: value
      })
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
