---
alwaysApply: true
---

## Mandate

Upon completing code changes and **before** submitting the final response, you must perform a self-correction pass. You must verify that the solution complies with all active governance files.


## Compliance Checklist


### 1. Core Python & Efficiency

* [ ] **Function Length:** Are all functions under 20 lines?

* [ ] **Parallelism:** Is `asyncio` used for I/O and `ProcessPoolExecutor` for CPU?

* [ ] **Typing:** Are all variables and functions fully type-hinted?

* [ ] **No Print:** Is the Logger used strictly?


### 2. Architecture & Agents

* [ ] **Nodes:** Do nodes follow Read -> Do -> Write -> Control?

* [ ] **Resilience:** Are external calls wrapped in `@retry` (Tenacity)?

* [ ] **Config:** Are no secrets hardcoded? Is `pydantic-settings` used?

* [ ] **Prompts:** Are prompts separated from code (Templates)?


### 3. RAG & Data (If Applicable)

* [ ] **Hybrid Search:** Is both keyword and vector search enabled?

* [ ] **Reranking:** Is a reranker step included?

* [ ] **Streaming:** Does the API support SSE/Streaming response?


### 4. Testing & Validation

* [ ] **Evals:** Are there Ragas/DeepEval metrics defined for the agent?

* [ ] **Unit Tests:** Do `pytest` tests pass with ✅ visuals?

* [ ] **Coverage:** Are edge cases covered?


### 5. Error Handling & Resilience

* [ ] **Error Classification:** Are errors properly classified (transient vs permanent)?

* [ ] **Retry Logic:** Are retries implemented with exponential backoff?

* [ ] **Circuit Breaker:** Are circuit breakers used for external services?

* [ ] **Graceful Degradation:** Does the system degrade gracefully on failures?

* [ ] **Error Logging:** Are errors logged with full context and structured format?


### 6. Performance & Optimization

* [ ] **Caching:** Are appropriate caching strategies implemented?

* [ ] **Query Optimization:** Are database queries optimized (indexes, no N+1 queries)?

* [ ] **Resource Pooling:** Are connections/resources pooled?

* [ ] **Connection Pooling:** Is connection pooling configured appropriately?


### 7. Documentation & API

* [ ] **API Docs:** Is OpenAPI/Swagger documentation complete?

* [ ] **Versioning:** Is API versioning strategy defined?

* [ ] **Examples:** Are request/response examples provided?

* [ ] **Error Responses:** Are error response schemas documented?


### 8. Deployment & Infrastructure

* [ ] **CI/CD:** Is CI/CD pipeline configured?

* [ ] **Containerization:** Are Docker images optimized (multi-stage builds, minimal size)?

* [ ] **Health Checks:** Are health check endpoints implemented?

* [ ] **Rollback Plan:** Is rollback procedure documented and tested?


## Note on Security

* Security and Environment isolation (`security-governance-and-observability.md`) are handled via a separate, strict enforcement layer.
