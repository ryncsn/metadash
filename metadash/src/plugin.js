import Plugins from '@/libs/metadash-plugins'

const PluginRoutes = []

for (let pluginName in Plugins) {
  let plugin = Plugins[pluginName]

  let pluginRoute = {
    path: '/' + plugin.path,
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
