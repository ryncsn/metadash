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
      msg: 'Plugins works!'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
</style>
