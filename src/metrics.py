import time
import json
from datetime import datetime
from collections import defaultdict

class MetricsRecorder:
    def __init__(self):
        self.records = []
        self.start_time = time.time()
        self.success_count = 0
        self.error_count = 0
        self.total_time = 0.0
        self.blocked_count = defaultdict(int)
        self.latencies = []

    def record_ok(self, category, latency, retries):
        if latency < 0:
            raise ValueError(f"Latencia negativa detectada. {latency}")

        self.success_count += 1
        self.latencies.append(latency)

        self.records.append({
            "timestamp": datetime.now().isoformat(),
            "status": "ok",
            "category": category,
            "latency": latency,
            "retries": retries,
        })

    def record_error(self, category, error_message, latency, retries):
        if latency < 0:
            raise ValueError(f"Latencia negativa detectada. {latency}")
        
        self.error_count += 1
        self.blocked_count[error_message] += 1
        self.latencies.append(latency)

        self.records.append({
            "timestamp": datetime.now().isoformat(),
            "status": "error",
            "category": category,
            "error_type": error_message,
            "latency": latency,
            "retries": retries,
        })

    def summary(self):
        self.total_time = time.time() - self.start_time
        total_requests = self.success_count + self.error_count

        avg_latency = (
            sum(self.latencies) / len(self.latencies)
            if self.latencies else 0
        )
    
        ok_rate = (
            ((self.success_count / total_requests) * 100)
            if total_requests else 0
        )

        return {
            "t_iterations": total_requests,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "ok_rate": round(ok_rate, 2),
            "avg_latency": round(avg_latency, 2),
            "total_time": round(self.total_time, 2),
            "blocked_count": dict(self.blocked_count),
        }