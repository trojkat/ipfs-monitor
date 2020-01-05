# IPFS Monitor

This tool aims for monitoring nodes and agent versions in the IPFS network.

[Here you can check](http://tagen.tv:5000) the IPFS Monitor in action.


## Requirements

* Docker
* IPFS node running on a host machine


## Running a IPFS Monitor instance

Run the IPFS node on a host machine (`ipfs daemon` in case of go-ipfs).

Run the IPFS Monitor in a docker container:

    docker-compose up -d

Download the first data sample:

    docker-compose exec monitor python ipfs_monitor/monitor.py

Go to the IPFS Monitor web app:

    http://localhost:5000

