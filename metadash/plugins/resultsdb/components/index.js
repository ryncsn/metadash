import overview from './overview.vue'
import testRun from './test-run.vue'
import testResult from './test-result.vue'

export default {
  path: '/resultsdb', // Need to be uniq, and will be used for url routing
  icon: '<i class="fa fa-cubes" aria-hidden="true"></i>', // Or import a webpack resource
  entry: overview,
  title: 'ResultsDB',
  children: [
    {
      path: '',
      component: overview
    },
    {
      path: 'test-run',
      component: testRun
    },
    {
      path: 'test-result',
      component: testResult
    }
  ]
}
