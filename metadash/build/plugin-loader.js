const path = require('path')
const glob = require('glob')
const fs = require('fs')

module.exports = function (source) {
  var pluginMetaPathes = glob.sync('metadash/plugins/*/plugin.json')
  var loadedPlugins = []

  var importSource = ''
  var declareSource = 'var Plugins = {\n'
  var exportSource = 'export default Plugins'

  for (let pluginIdx in pluginMetaPathes) {
    let pluginMeta = require(path.resolve(pluginMetaPathes[pluginIdx]))
    let pluginPath = path.resolve(path.dirname(pluginMetaPathes[pluginIdx]))
    let pluginEntryPath = path.join(pluginPath, 'components/index.js')
    if (!fs.existsSync(pluginEntryPath)) {
      console.log(`Skipped loading component of plugin ${pluginMeta.name}, since not component files founded`)
      continue
    }

    this.addDependency(pluginEntryPath)

    if (!pluginMeta.name) {
      throw Error(`Plugin ${pluginPath} don't have a valid name!`)
    }
    if (pluginMeta.name in loadedPlugins) {
      throw Error(`Plugin ${pluginMeta} name conflict!}`)
    }
    let moduleName = 'Module' + pluginIdx
    importSource += `import ${moduleName} from '${pluginEntryPath}'\n`
    declareSource += `  '${pluginMeta.name}': ${moduleName},\n`
    loadedPlugins.push(pluginMeta.name)
    console.log(`Loaded plugin ${pluginMeta.name}`)
  }
  declareSource += '}\n'
  return importSource + declareSource + exportSource
}
