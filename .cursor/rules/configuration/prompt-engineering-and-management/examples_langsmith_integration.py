"""
LangSmith Prompt Hub Integration Examples

This file demonstrates LangSmith Prompt Hub integration patterns.
Reference this example from RULE.mdc using @examples_langsmith_integration.py syntax.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime


# ============================================================================
# LangSmith Prompt Hub Integration
# ============================================================================

@dataclass
class PromptHubPrompt:
    """
    Prompt Hub prompt structure.
    
    This demonstrates Prompt Hub prompt:
    - Prompt ID and version
    - Content and metadata
    - Tags and descriptions
    - Performance metrics
    """
    prompt_id: str
    version: str
    content: str
    tags: List[str]
    description: str
    metadata: Dict[str, Any]
    created_at: datetime
    performance_metrics: Optional[Dict[str, float]] = None


class LangSmithPromptHubClient:
    """
    Client for LangSmith Prompt Hub.
    
    This demonstrates Prompt Hub integration:
    - Prompt registration
    - Prompt retrieval
    - Version management
    - Performance tracking
    """
    
    def __init__(self, api_key: str, project_name: str):
        """
        Initialize Prompt Hub client.
        
        Args:
            api_key: LangSmith API key
            project_name: Project name
        """
        self.api_key = api_key
        self.project_name = project_name
        # In real implementation:
        # from langsmith import Client
        # self.client = Client(api_key=api_key)
    
    def register_prompt(
        self,
        prompt_id: str,
        content: str,
        version: str = "1.0.0",
        tags: Optional[List[str]] = None,
        description: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> PromptHubPrompt:
        """
        Register prompt in Prompt Hub.
        
        Args:
            prompt_id: Prompt identifier
            content: Prompt content
            version: Version number
            tags: Optional tags
            description: Prompt description
            metadata: Optional metadata
        
        Returns:
            Registered PromptHubPrompt
        """
        # In real implementation:
        # prompt = self.client.create_prompt(
        #     name=prompt_id,
        #     version=version,
        #     prompt=content,
        #     tags=tags or [],
        #     metadata=metadata or {}
        # )
        
        # For example:
        prompt = PromptHubPrompt(
            prompt_id=prompt_id,
            version=version,
            content=content,
            tags=tags or [],
            description=description,
            metadata=metadata or {},
            created_at=datetime.now()
        )
        
        return prompt
    
    def get_prompt(
        self,
        prompt_id: str,
        version: Optional[str] = None,
        tag: Optional[str] = None
    ) -> Optional[PromptHubPrompt]:
        """
        Get prompt from Prompt Hub.
        
        Args:
            prompt_id: Prompt identifier
            version: Specific version (None for latest)
            tag: Tag filter (e.g., "production")
        
        Returns:
            PromptHubPrompt or None
        """
        # In real implementation:
        # if version:
        #     prompt = self.client.get_prompt(name=prompt_id, version=version)
        # else:
        #     prompt = self.client.get_prompt(name=prompt_id, tag=tag)
        
        # For example:
        return None
    
    def list_prompts(
        self,
        tags: Optional[List[str]] = None,
        limit: int = 100
    ) -> List[PromptHubPrompt]:
        """
        List prompts from Prompt Hub.
        
        Args:
            tags: Optional tag filters
            limit: Maximum number of results
        
        Returns:
            List of PromptHubPrompt
        """
        # In real implementation:
        # prompts = self.client.list_prompts(tags=tags, limit=limit)
        
        return []
    
    def update_prompt_metrics(
        self,
        prompt_id: str,
        version: str,
        metrics: Dict[str, float]
    ) -> bool:
        """
        Update prompt performance metrics.
        
        Args:
            prompt_id: Prompt identifier
            version: Version number
            metrics: Performance metrics
        
        Returns:
            True if update successful
        """
        # In real implementation:
        # self.client.update_prompt_metrics(
        #     name=prompt_id,
        #     version=version,
        #     metrics=metrics
        # )
        
        return True
    
    def deploy_prompt(
        self,
        prompt_id: str,
        version: str,
        tag: str = "production"
    ) -> bool:
        """
        Deploy prompt version with tag.
        
        Args:
            prompt_id: Prompt identifier
            version: Version to deploy
            tag: Deployment tag
        
        Returns:
            True if deployment successful
        """
        # In real implementation:
        # self.client.tag_prompt(
        #     name=prompt_id,
        #     version=version,
        #     tag=tag
        # )
        
        return True


# ============================================================================
# Prompt Registry with LangSmith
# ============================================================================

class PromptRegistry:
    """
    Prompt registry using LangSmith Prompt Hub.
    
    This demonstrates registry patterns:
    - Centralized prompt management
    - Version tracking
    - Runtime lookup
    - Performance monitoring
    """
    
    def __init__(self, hub_client: LangSmithPromptHubClient):
        """
        Initialize prompt registry.
        
        Args:
            hub_client: LangSmith Prompt Hub client
        """
        self.hub_client = hub_client
        self.cache: Dict[str, PromptHubPrompt] = {}
    
    def register(
        self,
        prompt_id: str,
        content: str,
        version: str = "1.0.0",
        tags: Optional[List[str]] = None,
        description: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> PromptHubPrompt:
        """
        Register prompt in registry.
        
        Args:
            prompt_id: Prompt identifier
            content: Prompt content
            version: Version number
            tags: Optional tags
            description: Prompt description
            metadata: Optional metadata
        
        Returns:
            Registered prompt
        """
        prompt = self.hub_client.register_prompt(
            prompt_id=prompt_id,
            content=content,
            version=version,
            tags=tags,
            description=description,
            metadata=metadata
        )
        
        # Cache for fast lookup
        cache_key = f"{prompt_id}:{version}"
        self.cache[cache_key] = prompt
        
        return prompt
    
    def get(
        self,
        prompt_id: str,
        version: Optional[str] = None,
        tag: str = "production"
    ) -> Optional[str]:
        """
        Get prompt content from registry.
        
        Args:
            prompt_id: Prompt identifier
            version: Specific version (None for tagged version)
            tag: Tag to use if version not specified
        
        Returns:
            Prompt content or None
        """
        # Check cache first
        cache_key = f"{prompt_id}:{version or tag}"
        if cache_key in self.cache:
            return self.cache[cache_key].content
        
        # Get from hub
        prompt = self.hub_client.get_prompt(
            prompt_id=prompt_id,
            version=version,
            tag=tag if not version else None
        )
        
        if prompt:
            # Cache for future use
            self.cache[cache_key] = prompt
            return prompt.content
        
        return None
    
    def lookup_by_tag(
        self,
        prompt_id: str,
        tag: str = "production"
    ) -> Optional[str]:
        """
        Lookup prompt by tag.
        
        Args:
            prompt_id: Prompt identifier
            tag: Tag (e.g., "production", "experimental")
        
        Returns:
            Prompt content or None
        """
        return self.get(prompt_id, tag=tag)
    
    def update_metrics(
        self,
        prompt_id: str,
        version: str,
        quality_score: float,
        latency: float,
        cost: float
    ):
        """
        Update prompt performance metrics.
        
        Args:
            prompt_id: Prompt identifier
            version: Version number
            quality_score: Quality score (0.0-1.0)
            latency: Latency in seconds
            cost: Cost in USD
        """
        metrics = {
            "quality_score": quality_score,
            "latency": latency,
            "cost": cost
        }
        
        self.hub_client.update_prompt_metrics(
            prompt_id=prompt_id,
            version=version,
            metrics=metrics
        )


# ============================================================================
# Runtime Integration
# ============================================================================

def get_prompt_from_registry(
    registry: PromptRegistry,
    prompt_id: str,
    environment: str = "production"
) -> str:
    """
    Get prompt from registry at runtime.
    
    This demonstrates runtime prompt retrieval:
    - Lookup from registry
    - Environment-based selection
    - Fallback handling
    
    Args:
        registry: Prompt registry
        prompt_id: Prompt identifier
        environment: Environment (production, staging, development)
    
    Returns:
        Prompt content
    """
    # Try to get prompt for environment
    prompt = registry.get(prompt_id, tag=environment)
    
    if prompt:
        return prompt
    
    # Fallback to production
    if environment != "production":
        prompt = registry.get(prompt_id, tag="production")
        if prompt:
            return prompt
    
    # Fallback to latest
    prompt = registry.get(prompt_id)
    if prompt:
        return prompt
    
    # Last resort: raise error
    raise ValueError(f"Prompt {prompt_id} not found in registry")
