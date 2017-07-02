<template>
  <div class="example">
    <h1>{{ msg }}</h1>
  </div>
</template>

<script>
export default {
  name: 'example',
  data () {
    return {
      msg: 'Plugin Works, will try to read from API...'
    }
  },
  methods: {
    refresh () {
      this.$http.get('/api/example/').then(res => {
        res.json().then(json => {
          this.msg = `Plugins works! Response: "${json[0].name}", created a entity with UUID ${json[0].uuid}`
        })
      })
    }
  },
  mounted () {
    this.refresh()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div {
  text-align: center;
}

h1, h2 {
  font-weight: normal;
}
</style>
