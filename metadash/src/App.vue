<template>
  <pf-layout id="app" :icons="true">
    <router-link slot="brand" to="/" :exact="true" class="navbar-brand">
      <span class="navbar-brand-name">Metadash</span>
    </router-link>

    <template slot="vertical-menu">
      <router-link tag="li" class="list-group-item" active-class="active" to="/dashboard" :exact="true">
        <a>
          <span class="fa fa-dashboard" title="Dashboard"></span>
          <span class="list-group-item-value">Dashboard</span>
        </a>
      </router-link>
      <router-link tag="li" class="list-group-item" active-class="active" to="/table" :exact="true">
        <a>
          <span class="fa fa-columns" title="Table"></span>
          <span class="list-group-item-value">Table</span>
        </a>
      </router-link>
    </template>
    <router-view></router-view>
  </pf-layout>
</template>

<script>
export default {
  name: 'app'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
