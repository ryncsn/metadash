from .config import Config


def load_meta(params, plugin_name=None):
    """
    Load metadata for configs
    Also create any missing configs
    """
    if params is None:
        return
    if not isinstance(params, (dict)):
        raise RuntimeError("configs have to be a dict, got {}, plugin {}"
                           .format(params, plugin_name))
    for key, item in params.items():
        if isinstance(item, str):
            item = {"default": item}
        if not isinstance(item, dict):
            raise RuntimeError("Parsing error: Unrecognized config parameters, "
                               "plugin {}, config {}".format(plugin_name, item))
        Config.create(key, plugin=plugin_name or "metadash", **item)
