<template>
  <div>
    <table class="table">
      <thead>
        <tr><td>Property</td><td>Value</td></tr>
      </thead>
      <tbody>
        <tr v-for="value, key in testrun.properties"><td> {{key}} </td> <td> {{value}} </td> </tr>
      </tbody>
    </table>

    <table class="table">
      <thead>
        <tr><td>Detail</td><td>Value</td></tr>
      </thead>
      <tbody>
        <tr v-for="value, key in testrun.details"><td> {{key}} </td> <td> {{value}} </td> </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: ['testrun'],
  data () {
    return {}
  }
}
</script>
</style>
