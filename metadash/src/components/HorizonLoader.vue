<template>
  <transition name="loading">
    <pacman-loader class="loading" v-if="loading" :loading="true"></pacman-loader>
  </transition>
</template>

<script>
/* A loading component */
import PacmanLoader from 'vue-spinner/src/PacmanLoader.vue'
export default {
  name: 'app',
  props: ['loading'],
  components: { PacmanLoader },
  data () {
    return {}
  }
}
</script>

<style scoped>
.loading {
  transition: all 0.2s ease-in;
  max-height: 70px;
  opacity: 1;
  width: 100px;
  margin: 10px auto;
  overflow: hidden;
}

.loading-enter-active, .loading-leave-active {
  transition: all 0.2s ease-out;
  max-height: 0px;
  opacity: 0;
}
</style>
