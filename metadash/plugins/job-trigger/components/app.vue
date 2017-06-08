<template>
  <div id='job-trigger'>
    <job-trigger>
    </job-trigger>
  </div>
</template>

<script>
import jobTrigger from './job-trigger'
export default {
  name: 'example',
  components: { jobTrigger }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
</style>
