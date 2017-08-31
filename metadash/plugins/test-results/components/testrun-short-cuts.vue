<template>
  <div>
    <button class="btn btn-primary btn-lg " type="button" :href="testrun.ref_url">Testrun Origin Link</button>
  </div>
</template>

<script>
export default {
  props: ['testrun'],
  data () {
    return {}
  },
  computed: {
    links () {
    }
  }
}
</script>
</style>
