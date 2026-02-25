"""
Base Watcher Class - Template for all watchers
All watchers inherit from this class to maintain consistency
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime


class BaseWatcher(ABC):
    """Abstract base class for all watchers"""

    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)

        # Create Needs_Action directory if it doesn't exist
        self.needs_action.mkdir(exist_ok=True)

        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    @abstractmethod
    def check_for_updates(self) -> list:
        """Return list of new items to process"""
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Create .md file in Needs_Action folder"""
        pass

    def run(self):
        """Main run loop - continuously monitors for updates"""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval} seconds')

        while True:
            try:
                items = self.check_for_updates()
                for item in items:
                    self.create_action_file(item)
            except KeyboardInterrupt:
                self.logger.info(f'{self.__class__.__name__} stopped by user')
                break
            except Exception as e:
                self.logger.error(f'Error in {self.__class__.__name__}: {e}')

            time.sleep(self.check_interval)

    def demo_run(self):
        """Demo run for testing without real data"""
        self.logger.info(f'Running {self.__class__.__name__} in demo mode')
