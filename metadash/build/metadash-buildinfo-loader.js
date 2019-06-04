const execSync = require('child_process').execSync
var currentVersion
var appRelativePath

try {
  currentVersion = String(execSync('git describe --always')).trim()
} catch (e) {
  currentVersion = 'unknown snapshot'
}

appRelativePath = process.env.APP_RELATIVE_PATH || ''

module.exports = function (source) {
  return `export default {
version: '(${currentVersion})',
relativePath: '${appRelativePath}',
}`
}
