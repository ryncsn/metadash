<template>
  <div>
    <pf-table :columns="columns" :rows="users">
      <template scope="scope">
        <td> {{ scope.row.username }} </td>
        <td v-for="role in roles">
          <bs-radio :checkedValue="role" :value="scope.row.role"
            @checked="setPermission(scope.row.username, role)"/>
          </td>
      </template>
    </pf-table>
  </div>
</template>
<script>
import _ from 'lodash'
export default {
  name: 'users',
  data () {
    return {
      'roles': ['admin', 'user', 'anonymous'],
      'users': [ ]
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    setPermission (username, role) {
      _.find(this.users, u => u.username === username).role = role
      this.$http.put('/api/users/' + username, { role: role })
        .then(() => this.debouncedRefresh())
        .catch(() => this.debouncedRefresh())
    },
    debouncedRefresh: _.debounce(function () {
      this.refresh()
    }, 500),
    refresh () {
      return this.$http.get('/api/users')
        .then(res => res.json())
        .then(data => {
          this.users = data
          this.savedUsers = JSON.parse(JSON.stringify(data))
        })
    }
  },
  computed: {
    columns () {
      return ['User'].concat(this.roles.map(_.upperFirst))
    },
    usernames () {
      return Object.keys(this.users)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
