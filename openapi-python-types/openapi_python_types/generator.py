"""Main generator module for converting OpenAPI specs to Python types."""

import json
from typing import Any

import yaml


def generate_types(spec_content: str, format: str = "auto") -> str:
    """Generate Python type definitions from an OpenAPI specification.
    
    Args:
        spec_content: The OpenAPI specification as a string (JSON or YAML)
        format: Format of the spec - "json", "yaml", or "auto" (default)
        
    Returns:
        Generated Python code with type definitions
    """
    # Parse the spec
    spec = parse_spec(spec_content, format)
    
    # Generate code
    generator = TypeGenerator(spec)
    return generator.generate()


def parse_spec(content: str, format: str = "auto") -> dict[str, Any]:
    """Parse an OpenAPI specification from JSON or YAML.
    
    Args:
        content: The specification content as a string
        format: Format of the spec - "json", "yaml", or "auto"
        
    Returns:
        Parsed specification as a dictionary
    """
    if format == "auto":
        # Try to detect format
        content_stripped = content.strip()
        if content_stripped.startswith("{"):
            format = "json"
        else:
            format = "yaml"
    
    if format == "json":
        return json.loads(content)
    else:
        return yaml.safe_load(content)


class TypeGenerator:
    """Generator for Python type definitions from OpenAPI schemas."""
    
    def __init__(self, spec: dict[str, Any]):
        self.spec = spec
        self.generated_types: set[str] = set()
        self.imports: set[str] = set()
        
    def generate(self) -> str:
        """Generate the complete Python code with type definitions."""
        lines = []
        
        # Generate schema types
        schemas = self.spec.get("components", {}).get("schemas", {})
        for name, schema in schemas.items():
            self.generate_schema_type(name, schema, lines)
        
        # Generate operation protocols
        paths = self.spec.get("paths", {})
        for path, path_item in paths.items():
            self.generate_path_operations(path, path_item, lines)
        
        # Build final output
        output = []
        
        # Add imports
        if self.imports:
            output.append(self._generate_imports())
            output.append("")
        
        # Add generated code
        output.extend(lines)
        
        return "\n".join(output)
    
    def _generate_imports(self) -> str:
        """Generate import statements."""
        imports = []
        
        # Group imports by module
        typing_imports = []
        for imp in sorted(self.imports):
            if imp.startswith("typing."):
                typing_imports.append(imp.split(".", 1)[1])
        
        if typing_imports:
            imports.append(f"from typing import {', '.join(sorted(typing_imports))}")
        
        return "\n".join(imports)
    
    def generate_schema_type(self, name: str, schema: dict[str, Any], lines: list[str]) -> None:
        """Generate a TypedDict for a schema object."""
        schema_type = schema.get("type")
        
        if schema_type == "object" or "properties" in schema:
            self._generate_typed_dict(name, schema, lines)
        elif "enum" in schema:
            self._generate_enum(name, schema, lines)
        elif "anyOf" in schema or "oneOf" in schema:
            self._generate_union(name, schema, lines)
    
    def _generate_typed_dict(self, name: str, schema: dict[str, Any], lines: list[str]) -> None:
        """Generate a TypedDict class."""
        self.imports.add("typing.TypedDict")
        
        properties = schema.get("properties", {})
        required = set(schema.get("required", []))
        
        # Check if we need NotRequired
        has_optional = any(prop_name not in required for prop_name in properties.keys())
        if has_optional:
            self.imports.add("typing.NotRequired")
        
        # Add docstring if description exists
        if "description" in schema:
            lines.append(f'"""{schema["description"]}"""')
        
        # Generate class definition
        lines.append(f"class {name}(TypedDict):")
        
        if not properties:
            lines.append("    pass")
        else:
            for prop_name, prop_schema in properties.items():
                prop_type = self._get_python_type(prop_schema)
                
                # Add NotRequired wrapper for optional fields
                if prop_name not in required:
                    prop_type = f"NotRequired[{prop_type}]"
                
                lines.append(f"    {prop_name}: {prop_type}")
        
        lines.append("")
    
    def _generate_enum(self, name: str, schema: dict[str, Any], lines: list[str]) -> None:
        """Generate a Literal type for an enum."""
        self.imports.add("typing.Literal")
        
        enum_values = schema.get("enum", [])
        
        # Format enum values based on type
        formatted_values = []
        for value in enum_values:
            if isinstance(value, str):
                formatted_values.append(f'"{value}"')
            else:
                formatted_values.append(str(value))
        
        lines.append(f"{name} = Literal[{', '.join(formatted_values)}]")
        lines.append("")
    
    def _generate_union(self, name: str, schema: dict[str, Any], lines: list[str]) -> None:
        """Generate a Union type for anyOf/oneOf."""
        self.imports.add("typing.Union")
        
        # Get the variants
        variants = schema.get("anyOf") or schema.get("oneOf", [])
        
        # Generate types for each variant
        variant_types = [self._get_python_type(variant) for variant in variants]
        
        lines.append(f"{name} = Union[{', '.join(variant_types)}]")
        lines.append("")
    
    def _get_python_type(self, schema: dict[str, Any]) -> str:
        """Convert an OpenAPI schema to a Python type string."""
        # Handle $ref
        if "$ref" in schema:
            ref = schema["$ref"]
            # Extract the type name from the reference
            return ref.split("/")[-1]
        
        # Handle nullable
        nullable = schema.get("nullable", False)
        
        # Get base type
        schema_type = schema.get("type")
        
        if schema_type == "string":
            if "enum" in schema:
                self.imports.add("typing.Literal")
                enum_values = [f'"{v}"' if isinstance(v, str) else str(v) for v in schema["enum"]]
                base_type = f"Literal[{', '.join(enum_values)}]"
            else:
                base_type = "str"
        elif schema_type == "integer":
            base_type = "int"
        elif schema_type == "number":
            base_type = "float"
        elif schema_type == "boolean":
            base_type = "bool"
        elif schema_type == "array":
            self.imports.add("typing.List")
            items_schema = schema.get("items", {})
            items_type = self._get_python_type(items_schema)
            base_type = f"List[{items_type}]"
        elif schema_type == "object":
            if "properties" in schema:
                # Inline object - use dict for now
                self.imports.add("typing.Dict")
                self.imports.add("typing.Any")
                base_type = "Dict[str, Any]"
            else:
                self.imports.add("typing.Dict")
                self.imports.add("typing.Any")
                base_type = "Dict[str, Any]"
        elif "anyOf" in schema:
            self.imports.add("typing.Union")
            variants = [self._get_python_type(v) for v in schema["anyOf"]]
            base_type = f"Union[{', '.join(variants)}]"
        elif "oneOf" in schema:
            self.imports.add("typing.Union")
            variants = [self._get_python_type(v) for v in schema["oneOf"]]
            base_type = f"Union[{', '.join(variants)}]"
        else:
            # Unknown type
            self.imports.add("typing.Any")
            base_type = "Any"
        
        # Add None for nullable
        if nullable:
            self.imports.add("typing.Optional")
            return f"Optional[{base_type}]"
        
        return base_type
    
    def generate_path_operations(self, path: str, path_item: dict[str, Any], lines: list[str]) -> None:
        """Generate Protocol classes for operations in a path."""
        # HTTP methods to check
        methods = ["get", "post", "put", "patch", "delete", "head", "options"]
        
        for method in methods:
            if method in path_item:
                operation = path_item[method]
                self._generate_operation_protocol(path, method, operation, lines)
    
    def _generate_operation_protocol(
        self, path: str, method: str, operation: dict[str, Any], lines: list[str]
    ) -> None:
        """Generate a Protocol for an API operation."""
        self.imports.add("typing.Protocol")
        self.imports.add("typing.Any")
        
        # Generate a name for the protocol
        operation_id = operation.get("operationId")
        if operation_id:
            protocol_name = f"{operation_id.replace('_', ' ').title().replace(' ', '')}Protocol"
        else:
            # Generate name from path and method
            path_name = path.strip("/").replace("/", "_").replace("{", "").replace("}", "")
            protocol_name = f"{method.title()}{path_name.title().replace('_', '')}Protocol"
        
        # Add description
        if "summary" in operation or "description" in operation:
            desc = operation.get("summary") or operation.get("description")
            lines.append(f'"""{desc}"""')
        
        lines.append(f"class {protocol_name}(Protocol):")
        lines.append(f'    """{method.upper()} {path}"""')
        lines.append("")
        lines.append("    def __call__(")
        lines.append("        self,")
        
        # Generate parameters
        params = []
        
        # Path parameters
        parameters = operation.get("parameters", [])
        for param in parameters:
            param_name = param.get("name", "")
            param_in = param.get("in", "")
            param_required = param.get("required", False)
            param_schema = param.get("schema", {})
            
            param_type = self._get_python_type(param_schema)
            
            if param_in == "path":
                params.append(f"        {param_name}: {param_type},")
            elif param_in == "query":
                if param_required:
                    params.append(f"        {param_name}: {param_type},")
                else:
                    self.imports.add("typing.Optional")
                    params.append(f"        {param_name}: Optional[{param_type}] = None,")
        
        # Request body
        request_body = operation.get("requestBody")
        if request_body:
            content = request_body.get("content", {})
            if "application/json" in content:
                body_schema = content["application/json"].get("schema", {})
                body_type = self._get_python_type(body_schema)
                params.append(f"        body: {body_type},")
        
        # Add parameters to method
        if params:
            lines.extend(params)
        
        # Return type
        responses = operation.get("responses", {})
        success_response = responses.get("200") or responses.get("201") or responses.get("204")
        
        if success_response:
            content = success_response.get("content", {})
            if "application/json" in content:
                response_schema = content["application/json"].get("schema", {})
                return_type = self._get_python_type(response_schema)
            else:
                return_type = "Any"
        else:
            return_type = "Any"
        
        lines.append(f"    ) -> {return_type}: ...")
        lines.append("")
