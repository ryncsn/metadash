<template>
  <div>
    <h1>{{ msg }}</h1>
    <router-view tag="button" class="btn btn-default btn-lg" type="button">
      Request A Machine
    </router-view>
  </div>
</template>

<script>
export default {
  data () {
    return {
      msg: 'Working in progress...'
    }
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
