# Run Evaluation Suite

## Overview
Execute the complete LLM evaluation suite using specialized evaluation frameworks (Ragas, DeepEval, LangSmith) to measure agent performance, quality, and compliance. This command provides comprehensive evaluation metrics for generative AI systems.

## Rules Applied
- `llm-evaluation-and-metrics` - LLM evaluation standards and mandatory metrics
- `llm-judge-protocol` - LLM Judge evaluation protocol and rubric
- `monitoring-and-observability` - LangSmith integration and tracing
- `data-schemas-and-interfaces` - Evaluation data structures and Pydantic schemas
- `error-handling-and-resilience` - Evaluation error handling and retry strategies
- `performance-optimization` - Evaluation performance metrics and optimization

## Steps

1. **Prepare Evaluation Environment**
   - **Evaluation Framework Validation**:
     - Verify evaluation frameworks are installed (Ragas, DeepEval, LangSmith)
     - Validate framework versions are compatible
     - Check framework configuration is correct
     - Verify framework dependencies are available
   - Check for golden dataset (`datasets/golden_qa.json` or similar)
   - Validate evaluation configuration and parameters
   - Ensure LangSmith tracing is enabled if applicable

2. **Execute Evaluation Metrics**
   - **Faithfulness**: Verify answers rely only on retrieved context (prevent hallucinations)
   - **Answer Relevance**: Check if answers address user prompts correctly
   - **Context Precision**: Validate retrieval step fetched relevant chunks
   - **Tool Usage Accuracy**: Evaluate agent tool selection and parameter validity
   - Run evaluation on golden dataset or specified test set

3. **Collect Evaluation Data**
   - Gather evaluation results from all frameworks
   - Collect LangSmith traces for LLM operations
   - **Cost Tracking**:
     - Extract token usage (input and output tokens per evaluation)
     - Calculate costs based on model pricing
     - Track cost per evaluation metric
     - Identify expensive evaluation operations
   - Extract performance metrics (latency, token usage, costs)
   - Capture evaluation execution logs
   - **Error Handling**: Classify evaluation errors as transient (retryable) or permanent (requires fix)

4. **Compare Against Golden Dataset**
   - Compare actual outputs with expected ideal answers (Ground Truth)
   - Calculate accuracy metrics and deviation scores
   - Identify cases where outputs don't match expectations
   - Analyze patterns in mismatches

5. **Analyze Evaluation Results**
   - Calculate average scores for each metric
   - Identify metrics below acceptable thresholds
   - Find specific test cases with poor performance
   - Detect systematic issues (e.g., consistent hallucination patterns)

6. **Generate Evaluation Report**
   - Create structured report with all metrics
   - Include per-metric breakdowns and scores
   - Highlight areas requiring improvement
   - Provide specific examples of failures or low scores
   - **Comparison with Previous Evaluations**:
     - Compare current metrics with previous evaluation runs
     - Identify metric trends (improving, degrading, stable)
     - Highlight significant changes in scores
     - Track evaluation cost trends over time
     - Provide trend analysis and recommendations

7. **Provide Improvement Recommendations**
   - Suggest prompt engineering improvements
   - Recommend retrieval strategy adjustments
   - Propose tool usage optimizations
   - Identify areas needing additional training data

## Data Sources
- Golden dataset (`datasets/golden_qa.json` or similar)
- Evaluation framework outputs (Ragas, DeepEval)
- LangSmith traces and evaluation runs
- Evaluation configuration files
- Previous evaluation results (for comparison)

## Output
A comprehensive evaluation report including:
- **Metric Scores**: Faithfulness, Answer Relevance, Context Precision, Tool Usage Accuracy
- **Comparison with Golden Dataset**: Accuracy metrics, deviation scores, mismatch patterns
- **Performance Metrics**: Latency, token usage, costs with cost tracking breakdown
- **Cost Analysis**: Cost per evaluation, cost trends, expensive operations identification
- **Evaluation Framework Validation**: Framework status, configuration validation, dependency checks
- **Specific Test Case Analysis**: Examples of failures or low scores with context
- **Trend Analysis**: Comparison with previous evaluations, metric trends, cost trends
- **Areas Requiring Improvement**: Prioritized by impact and severity
- **Actionable Recommendations**: Specific suggestions for each metric with implementation guidance
