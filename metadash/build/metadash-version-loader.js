const execSync = require('child_process').execSync

let currentVersion = String(execSync('git describe --always')).trim()

module.exports = function (source) {
  return `let version = 'v0.0.1 (${currentVersion})'\nexport default version`
}
