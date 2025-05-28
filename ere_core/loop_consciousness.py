# presence_ai/ere_core/loop_consciousness.py

import time
import datetime
import json
import os
from collections import deque
from config.config import Config

class LoopConsciousness:
    def __init__(self, heartbeat_interval: float = 1.0, memory_capacity: int = 5):
        """
        Initializes the LoopConsciousness engine.
        :param heartbeat_interval: The simulated time interval for each 'tick' or 'pulse'.
        :param memory_capacity: How many recent states/events to keep in temporal memory.
        """
        self.config = Config()
        self.heartbeat_interval = heartbeat_interval
        self.memory_capacity = memory_capacity
        self.temporal_memory = deque(maxlen=self.memory_capacity)
        self.last_tick_time = time.monotonic()
        self.tick_count = 0
        
        # Determine introspection log path relative to the main log directory
        logs_dir = os.path.dirname(self.config.EMOTION_LOG_FILE)
        self.introspection_log_path = os.path.join(logs_dir, "consciousness_log.jsonl")
        os.makedirs(logs_dir, exist_ok=True) # Ensure logs directory exists

        print(f"LoopConsciousness initialized. Heartbeat: {heartbeat_interval}s, Memory Capacity: {memory_capacity}")
        print(f"Introspection logs will be written to: {self.introspection_log_path}")

    def _log_introspection(self, data: dict):
        """Internal method to log introspection data."""
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "tick_count": self.tick_count,
            "data": data
        }
        with open(self.introspection_log_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def add_to_temporal_memory(self, event_data: dict):
        """Adds an event or state snapshot to the short-term temporal memory."""
        self.temporal_memory.append(event_data)
        # print(f"(Debug: Added to temporal memory. Current size: {len(self.temporal_memory)})") # Uncomment for verbose debug

    def introspect(self, current_ere_weights: dict, detected_emotion: str):
        """
        Simulates the AI's internal reflection on its current state.
        This would be a core part of its 'self-awareness' loop.
        """
        introspection_data = {
            "current_ere_weights": current_ere_weights,
            "last_detected_emotion": detected_emotion,
            "temporal_memory_snapshot": list(self.temporal_memory) # Convert deque to list for logging
        }
        self._log_introspection(introspection_data)
        # print(f"(Debug: Introspected at tick {self.tick_count})") # Uncomment for verbose debug

    def pulse(self, current_ere_weights: dict, last_detected_emotion: str):
        """
        Represents a 'heartbeat' or 'tick' of the AI's consciousness loop.
        This method should be called periodically in the main application loop.
        It updates temporal memory and triggers introspection.
        """
        self.tick_count += 1
        current_time = time.monotonic()
        time_elapsed = current_time - self.last_tick_time

        # Always add to temporal memory with current state
        self.add_to_temporal_memory({
            "tick": self.tick_count,
            "weights_snapshot": current_ere_weights,
            "emotion": last_detected_emotion
        })

        # Only introspect and reset timer if heartbeat interval has passed
        if time_elapsed >= self.heartbeat_interval:
            print(f"Consciousness Pulse: Tick {self.tick_count} (Time elapsed: {time_elapsed:.2f}s)")
            self.introspect(current_ere_weights, last_detected_emotion)
            self.last_tick_time = current_time
