// This file will be overrided by plugins-loader
// See build/plugin-loader.js for more detail
// Don't rename this file, and changing content have no effect.
const Plugins = {
  'plugin-name': {
    // The routing path for a plugin, should be unique
    path: 'plugin-routing-name',
    // Then main component for the plugin
    entry: '<Component>',
    // The icon for the plugin, currently need to be a meterial icon name
    icon: '<Element>',
    // Plugin name as it's title
    title: 'Plugin Name',
    // Which role is allowed to use this plugin, defaults to all ([anonymous, user, admin])
    // We only have three role and it's hard coded
    roles: [
      'anonymous',
      'user',
      'admin'
    ]
  }
}

export default Plugins
