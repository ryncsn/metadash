<template>
  <div>
    <h1>
      Test Run
    </h1>
  </div>
</template>

<script>
export default {
  name: 'test-run',
  props: ['uuid'],
  data () {
    return {}
  },
  mounted () {
    this.refresh()
  },
  methods: {
    refresh () {
      this.$http.get('/api/testruns/' + this.uuid)
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
