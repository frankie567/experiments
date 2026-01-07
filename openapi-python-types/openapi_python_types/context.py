"""Type definitions and context for the generator."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class GeneratorContext:
    """Context for the OpenAPI to Python type generation.
    
    This context is passed through all transformation functions and contains
    configuration options and state.
    """
    
    # Configuration options
    additional_properties: bool = False
    """Whether to allow additional properties on objects by default."""
    
    alphabetize: bool = False
    """Whether to alphabetize properties and operations."""
    
    array_length: bool = False
    """Whether to include tuple types with specific lengths for arrays with minItems/maxItems."""
    
    default_non_nullable: bool = True
    """Whether types are non-nullable by default (OpenAPI 3.1 behavior)."""
    
    empty_objects_unknown: bool = False
    """Whether empty objects should be typed as Dict[str, Any] or just an empty TypedDict."""
    
    exclude_deprecated: bool = False
    """Whether to exclude deprecated operations and schemas."""
    
    # State
    spec: dict[str, Any] = field(default_factory=dict)
    """The parsed OpenAPI specification."""
    
    imports: set[str] = field(default_factory=set)
    """Set of imports needed (e.g., 'List', 'Optional', 'TypedDict')."""
    
    def add_import(self, name: str) -> None:
        """Add an import to the context."""
        self.imports.add(name)
    
    def resolve_ref(self, ref: str) -> Any:
        """Resolve a $ref to its value in the spec.
        
        Args:
            ref: Reference string like "#/components/schemas/User"
            
        Returns:
            The resolved value from the spec
        """
        if not ref.startswith("#/"):
            raise ValueError(f"Only internal references are supported: {ref}")
        
        parts = ref[2:].split("/")
        current: Any = self.spec
        
        for part in parts:
            if isinstance(current, dict):
                value = current.get(part)
                if value is None:
                    raise ValueError(f"Cannot resolve reference: {ref}")
                current = value
            else:
                raise ValueError(f"Cannot resolve reference: {ref}")
        
        return current
    
    def get_ref_name(self, ref: str) -> str:
        """Extract the name from a reference and sanitize it.
        
        Args:
            ref: Reference string like "#/components/schemas/User"
            
        Returns:
            The sanitized name part (e.g., "User", "CostMetadataInput" from "CostMetadata-Input")
        """
        from .transform_components import _sanitize_schema_name
        
        name = ref.split("/")[-1]
        return _sanitize_schema_name(name)


@dataclass
class TransformOptions:
    """Options passed to each transform function."""
    
    ctx: GeneratorContext
    """The generator context."""
    
    path: str
    """The path in the OpenAPI spec (for debugging and naming)."""
    
    schema: dict[str, Any] | None = None
    """The current schema being transformed."""
