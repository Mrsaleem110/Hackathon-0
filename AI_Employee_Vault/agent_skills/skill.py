"""
Skill Base Class - Foundation for all agent skills
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SkillParameter:
    """Skill parameter definition"""
    name: str
    type: str  # 'string', 'number', 'boolean', 'object', 'array'
    description: str
    required: bool = True
    default: Any = None


class Skill(ABC):
    """Base class for all skills"""

    def __init__(
        self,
        name: str,
        description: str,
        group: str = 'general',
        version: str = '1.0.0',
    ):
        self.name = name
        self.description = description
        self.group = group
        self.version = version
        self.parameters: List[SkillParameter] = []
        self.execution_history: List[Dict] = []

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the skill"""
        pass

    def validate_parameters(self, **kwargs) -> bool:
        """Validate input parameters"""
        for param in self.parameters:
            if param.required and param.name not in kwargs:
                raise ValueError(f"Missing required parameter: {param.name}")
        return True

    def log_execution(self, params: Dict, result: Dict):
        """Log skill execution"""
        self.execution_history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'parameters': params,
            'result': result,
        })

    def get_manifest(self) -> Dict:
        """Get skill manifest for Claude Code"""
        return {
            'name': self.name,
            'description': self.description,
            'group': self.group,
            'version': self.version,
            'parameters': [
                {
                    'name': p.name,
                    'type': p.type,
                    'description': p.description,
                    'required': p.required,
                    'default': p.default,
                }
                for p in self.parameters
            ],
        }

    def get_execution_history(self) -> List[Dict]:
        """Get execution history"""
        return self.execution_history

    def clear_history(self):
        """Clear execution history"""
        self.execution_history = []
