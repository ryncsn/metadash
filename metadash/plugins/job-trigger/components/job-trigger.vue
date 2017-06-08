<template>
  <div>
    <div class="container">
      <form role="form">
        <div class="form-group">
          <br />
          <label for="job-trigger-form">Params for triggering a job</label>
          <br />
          <div class="input-group" v-bind:class="{ 'has-error': !archValid }" >
            <span class="input-group-addon" id="basic-addon1">Arch</span>
            <div class="tagsinput form-control">
              <span v-for="arch in arch" class="tag label label-info" v-on:click="removeArch(arch)">{{arch}} x</span>
            </div>
            <input type="text" class="form-control hidden" v-model="arch" placeholder="Arch" disabled="true">
            <div class="input-group-btn" style="z-index: 3;">
              <bs-dropdown text="Add">
                <ul slot="dropdown-menu" class="dropdown-menu dropdown-menu-right" role="menu">
                  <li v-for="arch in archCandidate"><a href="javascript:void(0)" v-on:click.stop.prevent="addArch(arch)">{{arch}}</a></li>
                </ul>
              </bs-dropdown>
            </div><!-- /btn-group -->
          </div>
          <br />

          <div class="input-group" v-bind:class="{ 'has-error': !ciMessageValid }" >
            <span class="input-group-addon" id="basic-addon1">CI Message</span>
            <input type="text" class="form-control" v-model="message" placeholder="CI Message: {'CI_TYPE': 'balbal'}">
          </div>
          <br />

          <div class="input-group">
            <span class="input-group-addon" id="basic-addon1" v-bind:class="{ 'has-error': !ciMessageValid }" >Package Name</span>
            <input type="text" class="form-control" v-model="pkg_name" placeholder="Package Name">
          </div>
          <br />

          <div class="input-group">
            <span class="input-group-addon" id="basic-addon1">Brew Tag</span>
            <input type="text" class="form-control" v-model="brew_tag" placeholder="Brew Tag">
          </div>
          <br />

          <div class="input-group">
            <span class="input-group-addon" id="basic-addon1">Product</span>
            <input type="text" class="form-control" v-model="product" placeholder="Product: eg: RHEL">
          </div>
          <br />

          <div class="input-group">
            <span class="input-group-addon" id="basic-addon1">Job name</span>
            <input type="text" class="form-control" v-model="job_name" placeholder="Job name">
          </div>
          <br />
        </div>

        <div class="well">
          Matched Jobs: {{ matchedJobs }}
        </div>

        <button type="submit" class="btn btn-default btn-lg pull-right" v-on:click.stop.prevent="submit">Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import Dropdown from 'vue-strap/src/Dropdown'
export default {
  components: { Dropdown },
  name: 'job-trigger',
  props: [ 'triggerGateUrl', 'getJobNamesUrl' ],
  data () {
    return {
      archCandidate: ['x86_64', 'ppc64le', 'aarch64'],
      tagCandidate: ['7.3', '7.4', 'arm'],

      pkg_name: '',
      arch: ['x86_64'],
      brew_tag: '',
      message: '{}',
      product: '',
      job_name: '',

      matchedJobs: []
    }
  },
  methods: {
    dataForSubmit () {
      // Send only follow keys and filter empty value
      return _.pickBy(
        _.pick(this, ['arch', 'brew_tag', 'message', 'product', 'job_name', 'pkg_name']),
        v => v !== '' && v.length !== 0
      )
    },
    submit () {
      this.$http.post('api/trigger-jobs', this.dataForSubmit())
        .then(() => {
          alert('Submit successful')
        }, (err) => {
          alert(`Failed with ${err.body}`)
        })
    },
    getMatchedJobs: _.debounce(function () {
      this.$http.post('api/get-jobs', this.dataForSubmit())
        .then((res) => {
          res.json().then((data) => {
            this.matchedJobs = data
          })
        }, (err) => {
          alert(`Failed with ${err.body}`)
        })
    }, 500),
    addArch (arch) {
      if (this.arch.indexOf(arch) === -1) {
        this.arch.push(arch)
      }
    },
    removeArch (arch) {
      this.arch.splice(this.arch.indexOf(arch), 1)
    },
    isJsonValid (str) {
      try {
        JSON.parse(str)
      } catch (e) {
        return false
      }
      return true
    }
  },
  computed: {
    archValid () {
      return (this.arch.length !== 0)
    },
    packageValid () {
      return true
    },
    productValid () {
      return true
    },
    jobNameValid () {
      return true
    },
    ciMessageValid () {
      return this.isJsonValid(this.message)
    }
  },
  created () {
  },
  watch: {
    job_name () {
      this.getMatchedJobs()
    },
    arch () {
      this.getMatchedJobs()
    },
    product () {
      this.getMatchedJobs()
    },
    brew_tag () {
      this.getMatchedJobs()
    },
    pkg_name () {
      this.getMatchedJobs()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.tagsinput {
  background-color: #fff;
  border: 1px solid #ccc;
  box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
  display: inline-block;
  padding: 0px 3px;
  color: #555;
  vertical-align: middle;
  border-radius: 4px;
  max-width: 100%;
  line-height: 22px;
  cursor: text;
}

.tagsinput input:focus {
  border: none;
  box-shadow: none;
}

.tagsinput .tag {
  margin-right: 2px;
  color: white;
  display: inline-block;
}
</style>
