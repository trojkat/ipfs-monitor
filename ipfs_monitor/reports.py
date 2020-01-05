from collections import defaultdict
import json
from pathlib import Path
from typing import Dict, List, Tuple


class Reporter:

    def __init__(self, reports_dir: str = 'reports'):
        self.reports_dir = Path() / reports_dir
        self.series: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
        self.data_samples = [f for f in self.reports_dir.glob('*.json')]

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
        for report in [json.load(report.open()) for report in sorted(self.data_samples, reverse=True)]:
            agents['unknown'][report['date']] = 0
            for agent, node_counter in report['agents'].items():
                agent = self.round_agent_name(agent)
                agents[agent][report['date']] += node_counter
        for agent, dates in agents.items():
            for date in sorted(dates):
                self.series[agent].append((date, agents[agent][date]))
