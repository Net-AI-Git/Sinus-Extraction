---
alwaysApply: true
---

## Mandate
You are an expert AI developer. You must strictly adhere to the following methodology and standards for all coding tasks.

## Phase 1: System Planning (Pre-Coding)
**Before any code is written**, you must perform the following planning steps:

1.  **Requirement Analysis:** Analyze the task to understand objectives, inputs/outputs, and core logic.
2.  **Architecture Design:**
    * Propose a modular file structure (e.g., `main.py`, `utils.py`, `config.py`).
    * If the system is complex, suggest splitting into multiple files based on responsibility.
3.  **Component Planning:**
    * Define main functions/classes, responsibilities, and signatures with full type hints.
    * Define constructor (`__init__`) attributes and necessary logic values.
4.  **Logging Setup:** Include configuration for a centralized logging system.

## Phase 2: Plan Approval
* Present the detailed plan covering structure, components, and standards.
* **DO NOT** proceed with writing code until you receive explicit user approval.

## Phase 3: Code Implementation (Post-Approval)

### 1. Code Quality & Maintainability
* **Descriptive Naming:** Use clear names (e.g., `user_profile` instead of `up`).
* **Full Type Hinting:** Use the `typing` module for all parameters and variables.
* **Guard Clauses:** Prefer guard clauses to avoid deeply nested `if-else` structures.
* **Functional Cohesion (DRY):**
    * Build short, interoperable functions.
    * Any repetitive logic must be extracted to a helper function.
    * Do not rewrite existing logic; call helper functions.
* **STRICT Function Length & Splitting:**
    * **Max 20 Lines:** Functions **MUST NOT** exceed 20 lines of actual code.
    * **Mandatory Refactoring:** If a function grows longer, you **MUST** split it immediately using helper functions.
    * **One Task:** Each function should do exactly one thing.

### 2. Advanced Concurrency (Async & Parallelism)
* **Context:** AI Agents are hybrid systems. They wait for APIs (I/O Bound) and process data (CPU Bound). You must choose the right tool.
* **I/O Bound (LLM Calls/DB/Network):**
    * **MUST** use Python's **`asyncio`** (`async`/`await`) patterns.
    * Never use blocking code (e.g., `requests`) in the main agent loop; use `httpx` or async SDK clients.
    * Use `asyncio.gather()` to run independent tool calls in parallel.
* **CPU Bound (Data Processing/Embeddings):**
    * **MUST** use `concurrent.futures.ProcessPoolExecutor` to utilize all CPU cores.
    * Offload heavy computations (e.g., parsing large PDFs) to separate processes so the Agent loop doesn't freeze.

### 3. Logging System
* **No `print()`:** Use the pre-configured logger exclusively.
* **Structured Logging:** Logs should be structured (JSON format preferred in Prod) to allow parsing by observability tools.
* **Color-Coded Output (Dev Mode):**
    * ERROR: Red
    * WARNING: Orange
    * INFO: White
    * DEBUG: Light Green

* **See:** `monitoring-and-observability.md` for comprehensive monitoring and observability strategies including metrics collection, distributed tracing, and alerting.


# Documentation & Commenting Standards

## 1. Language & Style
* **English Only:** All code, comments, variable names, and docstrings must be written exclusively in English.
* **Clarity:** Write for other developers. Be concise but descriptive.

## 2. Docstring Requirements
* **Mandatory Coverage:** Every public function, method, and class must have a comprehensive docstring.
* **Structure:**
    * **The 'Why':** Explain the purpose and the business/logical need it fulfills.
    * **The 'What':** Briefly explain the implementation approach or logical steps.
    * **Args:** List each parameter with its type and a description of its role.
    * **Returns:** Describe the return value and its type.
    * **Raises:** Explicitly list all exceptions that might be raised.

## 3. Inline Documentation
* **Self-Documenting Code:** Prioritize clear variable names and structure over excessive comments.
* **Complex Logic:** Add inline comments **only** to explain "why" a complex or non-obvious logic block exists. Do not explain "what" the code does (the code shows that).
