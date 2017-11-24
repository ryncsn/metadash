import app from './app.vue'
import overview from './overview.vue'
import testrunDetail from './testrun-detail.vue'
import testrunResults from './testrun-results.vue'
import testrunResultDetail from './testrun-result-detail.vue'
import testrunParameters from './testrun-parameters.vue'
import testrunDetailParameters from './testrun-detailed-parameters.vue'
import testrunShortCuts from './testrun-short-cuts.vue'
import testrunCompare from './testrun-compare.vue'
import testresultDetail from './testresult-detail.vue'

export default {
  path: 'test-results', // Need to be uniq, and will be used for url routing
  icon: '<i class="fa fa-cube" aria-hidden="true"></i>', // Or import a webpack resource
  entry: app,
  title: 'Test Results',
  children: [
    {
      path: 'testresult/:uuid/',
      component: testresultDetail,
      beforeEnter: (to, from, next) => {
        window.scrollTo(0, 0)
        next()
      },
      props: true
    },
    {
      path: 'testrun/:uuid/',
      component: testrunDetail,
      props: true,
      beforeEnter: (to, from, next) => {
        window.scrollTo(0, 0)
        next()
      },
      children: [
        {
          path: '',
          component: testrunResults
        },
        {
          path: 'results',
          component: testrunResults
        },
        {
          path: 'results/:name',
          component: testrunResultDetail
        },
        {
          path: 'parameters',
          component: testrunParameters
        },
        {
          path: 'details',
          component: testrunDetailParameters
        },
        {
          path: 'short-cuts',
          component: testrunShortCuts
        }
      ]
    },
    {
      path: 'testrun-compare/:src-uuid/:dst-uuid',
      component: testrunCompare,
      props: true
    },
    {
      path: '',
      component: overview,
      props: route => ({  // filter by url param
        filtersArg: Object.keys(route.query).map(key => ({
          label: key,
          name: key,
          value: route.query[key]
        }))
      })
    }
  ]
}
