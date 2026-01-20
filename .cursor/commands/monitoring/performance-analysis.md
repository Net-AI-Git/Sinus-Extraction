# Performance Analysis

## Overview
Comprehensive performance analysis to identify bottlenecks, optimize resource usage, and improve system efficiency. This command analyzes latency, throughput, resource consumption, and cache performance to provide actionable optimization recommendations.

## Rules Applied
- `performance-optimization` - Performance optimization strategies, caching, query optimization, resource pooling
- `monitoring-and-observability` - Performance metrics, SLI/SLO definitions, profiling
- `core-python-standards` - Concurrency patterns (asyncio, ProcessPoolExecutor)
- `error-handling-and-resilience` - Error impact on performance, error recovery performance
- `deployment-and-infrastructure` - Infrastructure performance, resource limits
- `rate-limiting-and-queue-management` - Queue performance, rate limiting impact

## Steps

1. **Latency Analysis**
   - **Percentile Analysis**:
     - Calculate P50, P95, P99 latency percentiles
     - Identify latency distribution patterns
     - Compare latency across different operations
   - **Operation Breakdown**:
     - Analyze latency by operation type (LLM calls, tool calls, database queries)
     - Identify slowest operations
     - Find latency bottlenecks
   - **Time Series Analysis**:
     - Track latency trends over time
     - Identify latency degradation patterns
     - Detect latency spikes and anomalies

2. **Throughput Analysis**
   - **Request Rate**:
     - Calculate requests per second/minute
     - Analyze throughput trends
     - Identify throughput bottlenecks
   - **Operation Throughput**:
     - Measure throughput by operation type
     - Identify low-throughput operations
     - Find throughput optimization opportunities
   - **Concurrency Analysis**:
     - Analyze concurrent request handling
     - Identify concurrency limits
     - Find parallelization opportunities

3. **Resource Usage Analysis**
   - **CPU Usage**:
     - Analyze CPU consumption patterns
     - Identify CPU-intensive operations
     - Find CPU optimization opportunities
   - **Memory Usage**:
     - Analyze memory consumption patterns
     - Identify memory leaks or excessive usage
     - Find memory optimization opportunities
   - **Network Usage**:
     - Analyze network bandwidth usage
     - Identify network-intensive operations
     - Find network optimization opportunities
   - **Database Usage**:
     - Analyze database connection usage
     - Identify database query patterns
     - Find database optimization opportunities

4. **Cache Performance Analysis**
   - **Cache Hit Rates**:
     - Calculate cache hit/miss ratios
     - Analyze cache effectiveness
     - Identify cache optimization opportunities
   - **Cache Patterns**:
     - Analyze cache usage patterns
     - Identify frequently cached data
     - Find cache strategy improvements
   - **Cache Configuration**:
     - Review cache TTL settings
     - Analyze cache invalidation strategies
     - Find cache configuration optimizations

5. **Query Optimization Analysis**
   - **Database Queries**:
     - Analyze query performance
     - Identify slow queries
     - Find N+1 query problems
   - **Index Usage**:
     - Analyze index effectiveness
     - Identify missing indexes
     - Find index optimization opportunities
   - **Query Patterns**:
     - Analyze query patterns
     - Identify inefficient query patterns
     - Find query optimization opportunities

6. **Connection Pooling Analysis**
   - **Pool Usage**:
     - Analyze connection pool utilization
     - Identify pool exhaustion patterns
     - Find pool sizing opportunities
   - **Pool Configuration**:
     - Review pool configuration
     - Analyze pool performance
     - Find pool optimization opportunities

7. **Bottleneck Identification**
   - **Critical Path Analysis**:
     - Identify critical execution paths
     - Find bottlenecks in critical paths
     - Prioritize optimizations
   - **Resource Contention**:
     - Identify resource contention points
     - Find contention resolution opportunities
   - **Sequential Dependencies**:
     - Identify unnecessary sequential operations
     - Find parallelization opportunities

8. **SLI/SLO Compliance Checks**
   - **Service Level Indicators**: Verify SLI metrics meet defined thresholds
   - **Service Level Objectives**: Check SLO compliance for all defined objectives
   - **SLO Violations**: Identify and analyze SLO violations
   - **SLO Trends**: Track SLO compliance trends over time

9. **Capacity Planning Recommendations**
   - **Resource Capacity**: Analyze current resource usage vs capacity
   - **Scaling Recommendations**: Provide scaling recommendations based on trends
   - **Capacity Projections**: Project future capacity needs
   - **Cost-Benefit Analysis**: Analyze cost vs performance trade-offs

10. **Performance Regression Detection**
    - **Baseline Comparison**: Compare current performance with historical baselines
    - **Regression Identification**: Identify performance regressions
    - **Regression Analysis**: Analyze causes of performance regressions
    - **Regression Trends**: Track regression patterns over time

11. **Generate Performance Report**
    - Create comprehensive performance analysis report
    - Include latency, throughput, and resource usage analysis
    - Provide cache and query optimization insights
    - Highlight bottlenecks and optimization opportunities
    - Include SLI/SLO compliance status
    - Provide capacity planning recommendations
    - Include performance regression analysis
    - Include prioritized recommendations
    - Provide specific optimization steps

## Data Sources
- Performance metrics from monitoring systems
- LangSmith traces (for LLM and tool call performance)
- Database query logs and performance metrics
- System resource usage metrics (CPU, memory, network)
- Cache performance metrics
- Application profiling data

## Output
A comprehensive performance analysis report including:
- **Latency Analysis**: Percentiles, operation breakdown, time series trends
- **Throughput Analysis**: Request rates, operation throughput, concurrency
- **Resource Usage**: CPU, memory, network, database usage patterns
- **Cache Performance**: Hit rates, patterns, configuration analysis
- **Query Optimization**: Database queries, index usage, query patterns
- **Connection Pooling**: Pool usage, configuration, optimization
- **Error Impact Analysis**: Error impact on performance, error recovery performance
- **Infrastructure Performance**: Infrastructure resource usage, resource limits
- **Queue Performance**: Queue metrics, rate limiting impact on performance
- **SLI/SLO Compliance**: SLI metrics, SLO compliance status, SLO violations, SLO trends
- **Capacity Planning**: Resource capacity analysis, scaling recommendations, capacity projections, cost-benefit analysis
- **Performance Regression**: Baseline comparison, regression identification, regression analysis, regression trends
- **Bottleneck Identification**: Critical paths, resource contention, sequential dependencies
- **Optimization Recommendations**: Prioritized suggestions with specific steps and impact assessment
- **Performance Baseline**: Current performance metrics for comparison
