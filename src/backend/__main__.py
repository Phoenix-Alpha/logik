import importlib

for module in [
    "infrastructure.dns.zone",
    "infrastructure.dns.certificate",
    # "infrastructure.database.aurora",
    # "infrastructure.amplify",
    "infrastructure.api",
    "infrastructure.storage.ftp",
]:
    importlib.import_module(module)
