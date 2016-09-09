#!/usr/bin/env bash
cd /var/services/homes/chengyanlai/GitRepo/TakeMeCamping
/bin/git pull
/bin/python ReserveAmericaScraper.py
/bin/cp index.htnl /volume1/web/
