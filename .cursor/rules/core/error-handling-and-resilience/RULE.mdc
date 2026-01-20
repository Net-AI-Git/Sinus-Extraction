---
alwaysApply: true
---

## 1. Error Classification

* **Transient Errors:** Errors that are temporary and may succeed on retry (e.g., network timeouts, rate limits, temporary service unavailability).
    * **Strategy:** Always retry transient errors with exponential backoff.
    * **Identification:** Use HTTP status codes (429, 503, 502), connection errors, or timeout exceptions.

* **Permanent Errors:** Errors that will not succeed on retry (e.g., authentication failures, invalid input, not found).
    * **Strategy:** Do not retry. Log the error and return appropriate error response to the user.
    * **Identification:** HTTP 4xx errors (except 429), validation errors, business logic errors.

* **Mandate:** Classify every error at the point of occurrence. Use typed exceptions or error codes to distinguish error types.

## 2. Retry Strategies

* **Exponential Backoff:** Increase wait time between retries exponentially (e.g., 1s, 2s, 4s, 8s).
    * **Base Delay:** Start with a base delay (e.g., 1 second).
    * **Max Delay:** Cap the maximum delay (e.g., 60 seconds) to prevent excessive waits.
    * **Max Attempts:** Limit the number of retry attempts (e.g., 3-5 attempts).

* **Jitter:** Add randomness to backoff delays to prevent thundering herd problems.
    * **Implementation:** Use `random.uniform(0, delay)` or `random.expovariate()` to add jitter.

* **Tenacity Integration:** Use the `@retry` decorator from Tenacity for automatic retry logic.
    * **Configuration:** Specify `stop`, `wait`, and `retry` conditions explicitly.
    * **Example:** `@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=60))`

* **Selective Retry:** Only retry on specific exceptions or conditions.
    * **Use `retry_if_exception_type()` or `retry_if_result()` to control retry behavior.

## 3. Circuit Breaker Pattern

* **Purpose:** Prevent cascading failures by stopping requests to a failing service.

* **States:**
    * **Closed:** Normal operation, requests pass through.
    * **Open:** Service is failing, requests are immediately rejected without calling the service.
    * **Half-Open:** Testing if service has recovered, allowing limited requests.

* **Configuration:**
    * **Failure Threshold:** Number of failures before opening the circuit (e.g., 5 failures).
    * **Timeout:** Time to wait before transitioning from Open to Half-Open (e.g., 60 seconds).
    * **Success Threshold:** Number of successful requests in Half-Open to close the circuit (e.g., 2 successes).

* **Implementation:** Use libraries like `circuitbreaker` or implement custom logic with state tracking.

## 4. Dead Letter Queues (DLQ)

* **Purpose:** Capture messages that fail processing after all retry attempts.

* **Use Cases:**
    * Failed API calls after max retries.
    * Messages that cannot be processed due to data corruption.
    * Business logic errors that require manual intervention.

* **Implementation:**
    * Store failed requests in a dedicated queue or database table.
    * Include full context: original request, error details, retry count, timestamp.
    * Provide monitoring and alerting for DLQ size.

* **Recovery:** Implement a process to review and reprocess DLQ items after fixing underlying issues.

## 5. Error Recovery Strategies

* **Graceful Degradation:** Provide reduced functionality when a service is unavailable.
    * **Example:** Return cached data when the primary data source is down.
    * **Example:** Disable non-critical features when dependencies fail.

* **Fallback Values:** Use default or cached values when primary sources fail.
    * **Example:** Use a default configuration when the config service is unavailable.

* **Partial Success:** Return partial results when some operations fail.
    * **Example:** Return successfully retrieved data even if some parallel requests failed.

* **User Communication:** Inform users about degraded functionality or temporary issues.

## 6. Error Logging & Context

* **Structured Logging:** Log errors in structured format (JSON) with full context.
    * **Required Fields:**
        * Error type and message
        * Stack trace
        * Request ID / Correlation ID
        * User ID (if applicable)
        * Timestamp
        * Service/component name
        * Error classification (transient/permanent)

* **Context Preservation:** Include all relevant context in error logs.
    * **Input parameters** (sanitized, no secrets)
    * **Request metadata** (headers, IP, user agent)
    * **System state** (retry count, circuit breaker state)

* **Sensitive Data:** Never log secrets, passwords, API keys, or PII in error messages.
    * Use masking or truncation for sensitive fields.

* **Error Aggregation:** Use error tracking tools (e.g., Sentry, Datadog) to aggregate and analyze errors.

## 7. Integration with LangGraph Nodes

* **State Management:** Append errors to a dedicated `errors` field in the state.
* **Error Routing:** Route persistent failures to dedicated error-handling or human review nodes.
* **State Reset:** On node success, reset `ERROR_COUNT=0` in the Global State.

* **See:** `langgraph-architecture-and-nodes.md` for node-specific error handling patterns.
