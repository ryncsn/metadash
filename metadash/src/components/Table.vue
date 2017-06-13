<template>
  <div>
    <pf-table :columns="columns" :rows="rows">
      <template scope="props">
        <td v-for="name in props.row"> {{name}} </td>
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
      page: 1,
      pages: 1,
      name: 'table',
      sortable: true,
      columns: [
        'Id',
        'Name',
        'Surname',
        'City',
        'State'
      ],
      rows: [
        {
          'Id': 1,
          'name': 'John',
          'surname': 'Smith',
          'city': 'New York',
          'state': 'New York'
        },
        {
          'Id': 2,
          'name': 'Joe',
          'surname': 'Black',
          'city': 'Miami',
          'state': 'Florida'
        }
      ]
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
