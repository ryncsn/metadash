"""
Kerberos helper
"""
import os
import metadash


# TODO: provide User.try_login
def kinit(username=None, password=None):
    """
    This assumes all plugin requires the same keytab, and the same global session.
    Which is not always true, but useful for some certain plugins.
    """
    ktab = metadash.config.Config.get("KERBEROS_KEYTAB_FILE")
    kprinciple = metadash.config.Config.get("KERBEROS_PRINCIPLE")
    if os.system("kinit -k -t {} {}".format(ktab, kprinciple)):
        raise RuntimeError("Kerberos Authentication Failed")
