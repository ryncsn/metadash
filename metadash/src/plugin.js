import Plugins from '@/libs/metadash-plugins'

const PluginRoutes = []

for (let pluginName in Plugins) {
  let plugin = Plugins[pluginName]

  if (plugin.path.indexOf('/') !== 0) {
    console.log("Plugin's path should start with '/'")
    plugin.path = '/' + plugin.path
  }

  let pluginRoute = {
    props: plugin.props,
    path: plugin.path,
    name: plugin.title,
    component: plugin.entry
  }
  if (plugin.children) {
    pluginRoute.children = plugin.children
  }

  PluginRoutes.push(pluginRoute)
}

export {
  Plugins,
  PluginRoutes
}
