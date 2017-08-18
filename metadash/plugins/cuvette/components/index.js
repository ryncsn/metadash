import component from './app.vue'
import overview from './overview.vue'
import requestMachine from './request-machine.vue'
import machineDetail from './machine-detail.vue'

export default {
  path: '/cuvette', // Need to be uniq, and will be used for url routing
  icon: '<i class="fa fa-eyedropper" aria-hidden="true"></i>', // Or import a webpack resource
  entry: component,
  title: 'Cuvette-Eyedropper',
  children: [
    {
      path: 'request',
      component: requestMachine
    },
    {
      path: 'machine/:hostname',
      component: machineDetail,
      props: true
    },
    {
      path: '',
      component: overview
    }
  ]

}
