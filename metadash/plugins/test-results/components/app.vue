<template>
  <div>
    <keep-alive>
      <router-view></router-view>
    </keep-alive>
  </div>
</template>

<script>
export default {
  name: 'testresult-navi',
  data () {
    return {}
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
pre {
  white-space: pre-wrap;       /* css-3 */
  white-space: -pre-wrap;      /* Opera 4-6 */
  white-space: -o-pre-wrap;    /* Opera 7 */
  white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
  word-wrap: break-word;       /* Internet Explorer 5.5+ */
}
</style>
