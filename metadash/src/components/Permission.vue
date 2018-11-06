<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="users"
      hide-actions
      class="elevation-1"
    >
      <template slot="items" slot-scope="props">
        <td>{{ props.item.username }}</td>
        <td>{{ props.item.role }}</td>
        <td class="layout px-0">
          <v-btn icon class="mx-0" @click="editItem(props.item)">
            <v-icon color="teal">edit</v-icon>
          </v-btn>
          <v-btn icon class="mx-0" @click="deleteItem(props.item)">
            <v-icon color="pink">delete</v-icon>
          </v-btn>
        </td>
      </template>
      <template slot="no-data">
        <v-alert :value="true" color="error" icon="warning">
          Sorry, nothing to display here :(
        </v-alert>
      </template>
    </v-data-table>
    <v-layout justify-center>
      <v-dialog v-model="showDialog" max-width="500px">
        <v-btn color="blue-grey lighten-2" dark slot="activator" class="mb-2">Create User</v-btn>
        <v-card>
          <v-card-title>
            <span class="headline">{{ formTitle }}</span>
          </v-card-title>
          <v-card-text>
            <v-container grid-list-md>
              <v-layout wrap>
                <v-flex xs12>
                  <v-text-field label="User Name" v-model="editedItem.username" :disabled="editingIndex !== -1"></v-text-field>
                </v-flex>
                <v-flex xs12>
                  <v-select :items="roles" v-model="editedItem.role" label="Roles" single-line></v-select>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" flat @click.native="closeEditDialog">Cancel</v-btn>
            <v-btn color="blue darken-1" flat @click.native="save">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>
  </div>
</template>

<script>
import _ from 'lodash'
export default {
  name: 'md-permission',
  data () {
    return {
      roles: [ 'admin', 'user', 'anonymous' ],
      users: [ ],
      showDialog: false,
      editingIndex: -1,
      headers: [
        { text: 'User Name', value: 'username' },
        { text: 'Role', value: 'role' },
        { text: 'Actions', value: 'name', sortable: false }
      ],
      editedItem: {
        username: '',
        role: 'anonymous'
      },
      defaultItem: {
        username: '',
        role: 'anonymous'
      }
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    createNewUser (username, role) {
      this.$mdAPI.post('/users/' + username, { role: role })
        .then(() => this.debouncedRefresh())
        .catch(() => this.debouncedRefresh())
    },
    deleteUser (username) {
      let res = confirm(`Delete user "${username}"?`)
      if (res) {
        this.$mdAPI.delete('/users/' + username)
          .then(() => this.debouncedRefresh())
          .catch(() => this.debouncedRefresh())
      }
      return res
    },
    setPermission (username, role) {
      this.$mdAPI.put('/users/' + username, { role: role })
        .then(() => this.debouncedRefresh())
        .catch(() => this.debouncedRefresh())
    },
    debouncedRefresh: _.debounce(function () {
      // TODO: Use event to avoid extra refresh
      this.refresh()
    }, 500),
    refresh () {
      this.$mdAPI.get('/users')
        .then(res => res.data)
        .then(data => {
          this.users = data
          this.savedUsers = JSON.parse(JSON.stringify(data))
        })
    },
    editItem (item) {
      this.editingIndex = this.users.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.showDialog = true
    },
    deleteItem (item) {
      this.deleteUser(item.username)
    },
    closeEditDialog () {
      this.showDialog = false
      this.editedItem = Object.assign({}, this.defaultItem)
      this.editingIndex = -1
    },
    save () {
      if (this.editingIndex > -1) {
        this.setPermission(this.editedItem.username, this.editedItem.role)
      } else {
        this.createNewUser(this.editedItem.username, this.editedItem.role)
      }
      this.closeEditDialog()
    }
  },
  computed: {
    usernames () {
      return Object.keys(this.users)
    },
    formTitle () {
      return this.editingIndex === -1 ? 'New User' : 'Update User Info'
    }
  },
  watch: {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
