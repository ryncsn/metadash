<template>
  <div>
    <pf-table class="toolbar-pf" :columns="columns" :rows="users">
      <template slot-scope="scope">
        <td> {{ scope.row.username }} </td>
        <td v-for="role in roles">
          <bs-radio :checkedValue="role" :value="scope.row.role"
            @checked="setPermission(scope.row.username, role)">
          </bs-radio>
        </td>
      </template>
      <template slot="action" slot-scope="scope">
        <button class="btn btn-danger" type="button" @click="deleteUser(scope.row.username)"> Delete User </button>
      </template>
    </pf-table>
    <div class="row toolbar-pf table-view-pf-toolbar">
      <div class="col-sm-12">
        <form class="toolbar-pf-actions">
          <div class="form-group create-user-button">
            <button class="btn btn-default" type="button" id="deleteRows1" @click="createNewUsers"> Create New Users </button>
          </div>
          <div class="form-group create-user-input">
            <bs-input v-model="newuser" class="create-user-input" placeholder="User names, split by ','"> </bs-input>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import _ from 'lodash'
export default {
  name: 'md-permission',
  data () {
    return {
      'roles': ['admin', 'user', 'anonymous'],
      'users': [ ],
      'newuser': ''
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    createNewUsers (username, role) {
      for (let username of this.newuser.split(',')) {
        this.$http.post('/api/users/' + username, { role: 'anonymous' })
          .then(() => this.debouncedRefresh())
          .catch(() => this.debouncedRefresh())
      }
      this.newuser = ''
    },
    deleteUser (username) {
      let res = confirm(`Delete user "${username}"?`)
      if (res) {
        this.$http.delete('/api/users/' + username)
          .then(() => this.debouncedRefresh())
          .catch(() => this.debouncedRefresh())
      }
    },
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
.create-user-button {
  padding-left: 0;
  width: 15%;
}
.create-user-input {
  min-width: 85%;
}
</style>
