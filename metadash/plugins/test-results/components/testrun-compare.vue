<template>
  <div>
    <horigizon-loader :loading='loading'> </horigizon-loader>
    <div>
      <h1>{{src}}</h1>
      <h1>{{dst}}</h1>
    </div>
  </div>
</template>

<script>
import HorigizonLoader from '@/components/HorizonLoader'
export default {
  components: { HorigizonLoader },
  props: ['src', 'dst'],
  data () {
    return {
      'loading': true,
      'oldTestrun': true,
      'newTestrun': true
    }
  },
  methods: {
    refresh () {
    }
  }
}
</script>
</style>
