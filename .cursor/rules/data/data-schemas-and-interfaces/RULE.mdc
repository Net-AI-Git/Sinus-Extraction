---
description: "Standards for Pydantic schemas, data models, and structured interfaces"
alwaysApply: false
---

## 1. Schema Definition Standards
* **Base Class:** Always inherit from `pydantic.BaseModel` for all data schemas.
* **Field Descriptions:** Every field MUST include a `Field(description="...")`. This is critical for the LLM to understand the parameter's meaning.
* **Type Hints:** Use standard Python types (`str`, `int`, `float`, `bool`).

## 2. Enforcing Constraints
* **Restricted Values:** Use `typing.Literal` for fields with finite options (e.g., operation modes).
    * *Do not* use generic strings when options are finite.

## 3. Reusability & Serialization
* **Inheritance:** Create base classes for shared fields to avoid duplication.
* **Serialization:** Rely on Pydantic's built-in `.json()` and `.parse_raw()` methods.

## 4. Integration with LLMs & Tools
* **Binding:** Use `.bind_tools(tools=[Schema])` when connecting schemas to LLMs.
* **Structured Outputs:** Always use structured outputs for tools, defining the schema with Pydantic models.
* **Method:** Use `with_structured_output()` where applicable.
* **Extraction:** Access arguments via `response.tool_calls[0]['args']` rather than parsing raw strings.

## Code Example Pattern

```python
from pydantic import BaseModel, Field
from typing import Literal

class BaseToolInput(BaseModel):
    user_id: str = Field(description="The ID of the user triggering the action")

class WeatherQuery(BaseToolInput):
    location: str = Field(description="City and state, e.g. San Francisco, CA")
    unit: Literal['celsius', 'fahrenheit'] = Field(description="Temperature unit")
