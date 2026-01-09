"""
Aura Lead Hunter - Rate Limiter
================================
Async rate limiting to avoid Telegram flood bans.
Implements exponential backoff and jittered delays.
"""

import asyncio
import random
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timedelta

from utils.logger import AuraLogger, ThoughtType


@dataclass
class RateLimitState:
    """Tracks rate limiting state."""
    last_action: Optional[datetime] = None
    consecutive_errors: int = 0
    is_flood_wait: bool = False
    flood_wait_until: Optional[datetime] = None


class RateLimiter:
    """
    Intelligent rate limiter with adaptive delays.
    Prevents Telegram flood bans using:
    - Jittered random delays
    - Exponential backoff on errors
    - Flood wait detection and handling
    """
    
    def __init__(
        self,
        min_delay: float = 2.0,
        max_delay: float = 5.0,
        logger: Optional[AuraLogger] = None
    ):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.logger = logger
        self.state = RateLimitState()
        
        # Separate limits for different action types
        self.action_delays = {
            "message_fetch": (1.0, 3.0),
            "join_chat": (30.0, 60.0),
            "send_message": (5.0, 10.0),
            "user_info": (0.5, 1.5),
        }
    
    def _log(self, action: str, details: dict) -> None:
        """Log rate limiting action."""
        if self.logger:
            self.logger.thought(
                ThoughtType.RATE_LIMIT,
                "RateLimiter",
                action,
                details
            )
    
    async def wait(self, action_type: str = "default") -> float:
        """
        Wait for appropriate delay before next action.
        Returns the actual delay used.
        """
        # Check if we're in flood wait state
        if self.state.is_flood_wait and self.state.flood_wait_until:
            if datetime.now() < self.state.flood_wait_until:
                remaining = (self.state.flood_wait_until - datetime.now()).total_seconds()
                self._log(
                    "Waiting for flood ban to expire",
                    {"remaining_seconds": remaining}
                )
                await asyncio.sleep(remaining + random.uniform(1, 5))
                self.state.is_flood_wait = False
                self.state.flood_wait_until = None
        
        # Get delay range for action type
        if action_type in self.action_delays:
            min_d, max_d = self.action_delays[action_type]
        else:
            min_d, max_d = self.min_delay, self.max_delay
        
        # Apply exponential backoff if there were errors
        if self.state.consecutive_errors > 0:
            backoff_multiplier = min(2 ** self.state.consecutive_errors, 32)
            min_d *= backoff_multiplier
            max_d *= backoff_multiplier
            self._log(
                "Applying exponential backoff",
                {
                    "consecutive_errors": self.state.consecutive_errors,
                    "multiplier": backoff_multiplier
                }
            )
        
        # Jittered delay
        delay = random.uniform(min_d, max_d)
        
        self._log(
            f"Sleeping before {action_type}",
            {"delay_seconds": round(delay, 2)}
        )
        
        await asyncio.sleep(delay)
        self.state.last_action = datetime.now()
        
        return delay
    
    async def handle_flood_wait(self, wait_seconds: int) -> None:
        """
        Handle Telegram FloodWait error.
        Sets state to wait until flood ban expires.
        """
        self.state.is_flood_wait = True
        self.state.flood_wait_until = datetime.now() + timedelta(seconds=wait_seconds)
        self.state.consecutive_errors += 1
        
        self._log(
            "FLOOD WAIT triggered!",
            {
                "wait_seconds": wait_seconds,
                "resume_at": self.state.flood_wait_until.isoformat()
            }
        )
        
        # Add buffer to be safe
        await asyncio.sleep(wait_seconds + random.uniform(5, 15))
        
        self.state.is_flood_wait = False
        self.state.flood_wait_until = None
    
    def report_success(self) -> None:
        """Report successful action, reduces backoff."""
        if self.state.consecutive_errors > 0:
            self.state.consecutive_errors = max(0, self.state.consecutive_errors - 1)
    
    def report_error(self) -> None:
        """Report failed action, increases backoff."""
        self.state.consecutive_errors += 1
    
    async def batch_delay(self, batch_size: int, items_processed: int) -> None:
        """
        Additional delay after processing a batch of items.
        Helps avoid rate limits during bulk operations.
        """
        if items_processed > 0 and items_processed % batch_size == 0:
            delay = random.uniform(5.0, 15.0)
            self._log(
                f"Batch delay (every {batch_size} items)",
                {"items_processed": items_processed, "delay_seconds": round(delay, 2)}
            )
            await asyncio.sleep(delay)


def create_rate_limiter(
    min_delay: float = 2.0,
    max_delay: float = 5.0,
    logger: Optional[AuraLogger] = None
) -> RateLimiter:
    """Factory function to create rate limiter with settings."""
    return RateLimiter(min_delay, max_delay, logger)
