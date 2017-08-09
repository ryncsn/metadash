<template>
  <div>
    <table class="table">
      <thead>
        <tr><td>Property</td><td>Value</td></tr>
      </thead>
      <tbody>
        <tr v-for="key in Object.keys(testrun.properties)"><td> {{key}} </td> <td> {{testrun.properties[key]}} </td> </tr>
      </tbody>
    </table>

    <table class="table">
      <thead>
        <tr><td>Detail</td><td>Value</td></tr>
      </thead>
      <tbody>
        <tr v-for="key in Object.keys(testrun.details)"><td> {{key}} </td> <td> {{testrun.details[key]}} </td> </tr>
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
