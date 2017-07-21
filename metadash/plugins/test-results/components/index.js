import app from './app.vue'
import overview from './overview.vue'
import testrunDetail from './testrun-detail.vue'
import testresultDetail from './testresult-detail.vue'

export default {
  path: 'test-results', // Need to be uniq, and will be used for url routing
  icon: '<i class="fa fa-cube" aria-hidden="true"></i>', // Or import a webpack resource
  entry: app,
  title: 'Test Results',
  children: [
    {
      path: 'testresult/:uuid',
      component: testresultDetail,
      props: true
    },
    {
      path: 'testrun/:uuid',
      component: testrunDetail,
      props: true
    },
    {
      path: '',
      component: overview
    }
  ]
}
