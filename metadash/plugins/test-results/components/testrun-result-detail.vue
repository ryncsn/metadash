<template>
  <div v-if="data">
    <div v-for="value, key in data.properties">
      <h2> {{key}} </h2>
      <h6 v-for="line in value.split('|')"> {{line}} </h6>
    </div>
    <div v-for="value, key in data.details">
      <h2> {{key}} </h2>
      <h6 v-for="line in value.split('|')"> {{line}} </h6>
    </div>
  </div>
</template>

<script>
export default {
  props: ['uuid'],
  data () {
    return {
      data: {}
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    refresh () {
      this.$http.get(`/api/testresults/${this.uuid}`)
        .then(res => res.json())
        .then(data => {
          this.data = data
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
