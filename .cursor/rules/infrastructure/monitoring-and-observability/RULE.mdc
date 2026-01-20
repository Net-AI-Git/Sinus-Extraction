---
description: "Standards for metrics, logging, tracing, and observability"
alwaysApply: false
---

## 1. Metrics Collection

* **Prometheus Integration:** Use Prometheus for metrics collection in production.
    * **Counter:** Track cumulative metrics (e.g., total requests, errors).
    * **Gauge:** Track values that can go up or down (e.g., active connections, queue size).
    * **Histogram:** Track distributions (e.g., request duration, response size).
    * **Summary:** Track quantiles over time windows.

* **StatsD Integration:** Use StatsD for lightweight metrics collection.
    * **Format:** `metric_name:value|type|@sample_rate`
    * **Types:** `c` (counter), `g` (gauge), `ms` (timer), `h` (histogram).

* **Mandatory Metrics:**
    * **Request Rate:** Requests per second/minute.
    * **Error Rate:** Errors per second/minute.
    * **Latency:** P50, P95, P99 percentiles.
    * **Throughput:** Successful operations per time unit.
    * **Resource Usage:** CPU, memory, disk, network.

* **Custom Business Metrics:** Track domain-specific metrics (e.g., LLM token usage, agent step count, tool call success rate).

## 2. Distributed Tracing

* **OpenTelemetry Integration:** Use OpenTelemetry for distributed tracing.
    * **Spans:** Create spans for each operation (API calls, database queries, LLM calls).
    * **Trace Context:** Propagate trace context across service boundaries (HTTP headers, gRPC metadata).
    * **Span Attributes:** Add relevant attributes (user ID, request ID, operation type).

* **Trace Sampling:** Implement sampling to reduce overhead in high-traffic scenarios.
    * **Strategy:** Sample a percentage of traces (e.g., 10%) or use adaptive sampling based on error rates.

* **Integration Points:**
    * **FastAPI:** Use OpenTelemetry FastAPI instrumentation.
    * **Database:** Instrument database drivers (SQLAlchemy, asyncpg).
    * **HTTP Clients:** Instrument httpx, aiohttp for outbound requests.
    * **LangChain:** Use LangSmith for LLM operation tracing.

## 3. Log Aggregation Strategies

* **Centralized Logging:** Send all logs to a centralized system (e.g., ELK Stack, Loki, CloudWatch).
    * **Structured Format:** Use JSON format for logs to enable parsing and querying.
    * **Log Levels:** Use appropriate levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).

* **Correlation IDs:** Include correlation/request IDs in all log entries to trace requests across services.
    * **Propagation:** Pass correlation IDs through HTTP headers, message queues, and async operations.

* **Log Retention:** Define retention policies based on log level and importance.
    * **Production:** Retain ERROR and above for extended periods (e.g., 90 days).
    * **Development:** Shorter retention for DEBUG logs.

* **See:** `core-python-standards.md` for structured logging implementation details.

## 4. Alerting Rules & Thresholds

* **Alert Definition:**
    * **Thresholds:** Define clear thresholds for alerting (e.g., error rate > 5%, latency P99 > 1s).
    * **Duration:** Require threshold violation for a duration before alerting (e.g., 5 minutes).
    * **Severity:** Classify alerts by severity (critical, warning, info).

* **Alert Targets:**
    * **Critical:** Page on-call engineers (PagerDuty, Opsgenie).
    * **Warning:** Send to Slack/email channels.
    * **Info:** Log only, no notification.

* **Alert Fatigue Prevention:**
    * **Grouping:** Group similar alerts to avoid spam.
    * **Suppression:** Suppress alerts during known maintenance windows.
    * **Escalation:** Escalate unacknowledged critical alerts.

* **SLI/SLO-Based Alerts:** Base alerts on Service Level Indicators (SLI) and Service Level Objectives (SLO).
    * **Example:** Alert if error budget consumption rate exceeds threshold.

## 5. Performance Profiling

* **Application Profiling:** Use profiling tools to identify performance bottlenecks.
    * **Python Profilers:** Use `cProfile`, `py-spy`, or `pyinstrument` for CPU profiling.
    * **Memory Profiling:** Use `memory_profiler` or `py-spy` for memory analysis.

* **Production Profiling:** Enable continuous profiling in production (e.g., Pyroscope, Datadog Continuous Profiler).
    * **Sampling:** Use sampling to minimize overhead (e.g., 100Hz sampling rate).

* **Key Areas to Profile:**
    * **LLM API Calls:** Track latency and token usage.
    * **Database Queries:** Identify slow queries and N+1 problems.
    * **Tool Execution:** Profile tool call duration and resource usage.

## 6. Health Check Endpoints

* **Liveness Probe:** Endpoint that indicates if the service is running.
    * **Path:** `/health/live` or `/healthz`
    * **Response:** Simple 200 OK if service is alive.

* **Readiness Probe:** Endpoint that indicates if the service is ready to accept traffic.
    * **Path:** `/health/ready` or `/ready`
    * **Checks:** Verify database connectivity, external service availability, resource availability.
    * **Response:** 200 OK if ready, 503 if not ready.

* **Startup Probe:** Endpoint for services with long startup times.
    * **Path:** `/health/startup`
    * **Use:** Allow service time to initialize before marking as ready.

* **Implementation:** Use FastAPI dependency injection to check dependencies.
    * **Cache Results:** Cache health check results for a short duration (e.g., 5 seconds) to avoid excessive checks.

## 7. SLI/SLO Definitions

* **Service Level Indicators (SLI):** Measurable aspects of service quality.
    * **Examples:**
        * **Availability:** Percentage of successful requests.
        * **Latency:** P95 or P99 response time.
        * **Error Rate:** Percentage of requests that result in errors.
        * **Throughput:** Requests per second.

* **Service Level Objectives (SLO):** Target values for SLIs.
    * **Example:** 99.9% availability, P95 latency < 500ms, error rate < 0.1%.

* **Error Budget:** The acceptable amount of service degradation.
    * **Calculation:** 100% - SLO (e.g., 0.1% error budget for 99.9% availability).
    * **Usage:** Track error budget consumption and alert when approaching limits.

* **Documentation:** Document SLIs, SLOs, and error budgets for all services.

## 8. Integration with LangSmith

* **Tracing LLM Operations:** Use LangSmith to trace LangChain operations.
    * **Configuration:** Set `LANGCHAIN_TRACING_V2=true` and provide API key.
    * **Automatic Tracing:** LangChain automatically traces LLM calls, tool calls, and agent steps.

* **Evaluation Tracking:** Track LLM evaluation results in LangSmith.
    * **Link Evaluations:** Link evaluation runs to specific traces for analysis.

* **See:** `security-governance-and-observability.md` for auditing requirements that complement LangSmith tracing.
