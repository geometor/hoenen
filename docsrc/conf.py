from pathlib import Path

from photon_platform.publish.global_conf import *
import geometor.hoenen as module

version = module.__version__

org = "geometor"
org_name = "GEOMETOR"

repo = "hoenen"
repo_name = "hoenen"

setup_globals(org, org_name, repo, repo_name)

site_title = "Peter Hoenen, S.J."
project = site_title
html_title = f"{site_title} • {org_name}"
author = "Petrus Hoenen, S.J."
copyright = "1954, Pontificia Universitas Gregoriana • Digital Edition GEOMETOR"

# Restrict intersphinx_mapping strictly to local inventories present on disk
for _key in list(intersphinx_mapping.keys()):  # noqa: F405
    _entry = intersphinx_mapping[_key]  # noqa: F405
    _target = _entry[1] if isinstance(_entry, tuple) and len(_entry) >= 2 else None
    _local_file = _target[0] if isinstance(_target, tuple) and _target else _target
    if not (isinstance(_local_file, str) and Path(_local_file).is_file()):
        intersphinx_mapping.pop(_key, None)  # noqa: F405
