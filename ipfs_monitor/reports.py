from collections import defaultdict
from datetime import datetime
import json
from pathlib import Path
from typing import Dict, List, Tuple


class Reporter:

    def __init__(self, reports_dir: str = 'reports', data_samples_limit: int = 48):
        self.reports_dir = Path() / reports_dir
        self.series: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
        self.data_samples = sorted([f for f in self.reports_dir.glob('*.json')], reverse=True)[:data_samples_limit]
        self.latest_agents: Dict[str, int] = {}
        self.last_update = None

    @staticmethod
    def round_agent_name(name: str) -> str:
        if not name:
            return 'unknown'
        if name.startswith('go-ipfs') or name.startswith('/go-ipfs'):
            name, version, _ = name.lstrip('/').split('/')
            major, minor, _ = version.split('.')
            return f'{name}/{major}.{minor}.x'
        return 'other'

    def generate_report(self):
        agents: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        for i, report in enumerate([json.load(report.open()) for report in self.data_samples]):
            if i == 0:
                self.latest_agents = report['agents']
                self.last_update = datetime.fromisoformat(report['date']).strftime('%Y-%m-%d %H:%M')
            agents['unknown'][report['date']] = 0
            for agent, node_counter in report['agents'].items():
                agent = self.round_agent_name(agent)
                agents[agent][report['date']] += node_counter
        for agent, dates in agents.items():
            for date in sorted(dates):
                self.series[agent].append((date, agents[agent][date]))
