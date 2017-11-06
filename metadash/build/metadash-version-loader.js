const execSync = require('child_process').execSync
var currentVersion

try {
  currentVersion = String(execSync('gitscribe --always')).trim()
} catch (e) {
  currentVersion = ''
}

module.exports = function (source) {
  return `let version = 'v0.0.1 (${currentVersion})'\nexport default version`
}
