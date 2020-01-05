from collections import defaultdict
from datetime import datetime
import json
from typing import Dict, List, Optional

import ipfshttpclient


class IpfsMonitor:

    def __init__(self):
        self._client: ipfshttpclient = ipfshttpclient.connect(session=True)
        self.peers: List[str] = []
        self.protocols: Dict[str, int] = defaultdict(int)
        self.agents: Dict[str, int] = defaultdict(int)

    def get_active_peers(self) -> List[str]:
        self.peers = [item['Peer'] for item in self._client.swarm.peers()['Peers']]
        print(f'Found {len(self.peers)} active peers')

    def scan_peers(self):
        peers_to_scan = len(self.peers)
        for index, peer in enumerate(self.peers):
            print(f'Scaning peer {index + 1}/{peers_to_scan}')
            try:
                details = self._client.id(peer=peer, timeout=2)
            except ipfshttpclient.exceptions.TimeoutError:
                print('Timeout')
                continue
            self.protocols[details['ProtocolVersion']] += 1
            self.agents[details['AgentVersion']] += 1

    def sort_agents(self):
        self.agents = {k: v for k, v in sorted(self.agents.items(), key=lambda item: item[1], reverse=True)}

    def save_report(self, filename: Optional[str] = None):
        date_str = datetime.utcnow().isoformat()[:19]
        data = {
            'date': date_str,
            'agents': self.agents,
            'protocols': self.protocols,
        }
        json_str = json.dumps(data, indent=2)
        if not filename:
            filename = f'reports/{date_str}'
        with open(f'{filename}.json', 'w') as output_file:
            output_file.write(json_str)


if __name__ == '__main__':
    monitor = IpfsMonitor()
    monitor.get_active_peers()
    monitor.scan_peers()
    monitor.sort_agents()
    monitor.save_report()
