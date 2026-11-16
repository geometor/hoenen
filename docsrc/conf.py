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
