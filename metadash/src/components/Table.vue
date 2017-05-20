<template>
  <div class="hello">
    <pf-table :columns="columns" :rows="rows">
    </pf-table>
  </div>
</template>

<script>
export default {
  data () {
    return {
      columns: [
        'Test',
        'Result'
      ],
      rows: [
        {
          'test': 'T1',
          'result': 'Pass'
        },
        {
          'test': 'T2',
          'result': 'Pass'
        }
      ]
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
