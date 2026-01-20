# Cursor Rules Documentation

This directory contains Cursor Rules - system-level instructions for the Cursor AI Agent. Rules define coding standards, architectural patterns, security requirements, and development workflows that guide the AI's behavior.

## What are Cursor Rules?

Cursor Rules provide system-level instructions to the Cursor AI Agent. They bundle prompts, scripts, and more together, making it easy to manage and share workflows across your team. Rules are stored in `.cursor/rules` and are version-controlled.

Rules are included at the start of the model context, giving the AI consistent guidance for generating code, interpreting edits, or helping with workflows.

## Directory Structure

Rules in this repository are organized by category:

```
.cursor/rules/
├── core/              # Always-applied core rules (Python standards, error handling)
├── security/          # Security and governance rules
├── agents/            # Agent-specific rules (multi-agent, LangGraph, agentic logic)
├── infrastructure/    # Deployment, monitoring, performance
├── development/       # Testing, code review, versioning
├── api/               # API-related rules
├── data/              # Data schemas, migrations
├── evaluation/        # LLM evaluation, judging, auditing
├── configuration/     # Configuration, dependency injection, prompts
├── rules-management/ # Meta-rule for managing rules
└── commands-management/ # Meta-rule for managing commands
```

### Rule Folder Structure

Each rule is a **folder** containing a `RULE.md` file:

```
.cursor/rules/
  category-name/
    rule-name/
      RULE.md
```

**Important:**
- Each rule must be in its own folder
- The folder name should be kebab-case (e.g., `core-python-standards`)
- The file inside must be named exactly `RULE.md` (capital letters)

## Rule Types

Rules are applied automatically based on their type, defined in the YAML frontmatter at the start of each `RULE.md` file:

### 1. Always Apply

Applied to every chat session automatically.

**Frontmatter:**
```yaml
---
alwaysApply: true
---
```

**Use when:** The rule should always be active (e.g., core coding standards, security requirements).

**Examples:**
- `core-python-standards` - Python coding standards
- `error-handling-and-resilience` - Error handling patterns
- `security-governance-and-observability` - Security standards
- `audit-protocol` - Audit procedures
- `final-review-protocol` - Final review process

### 2. Apply Intelligently

Applied when the Agent decides it's relevant based on the description.

**Frontmatter:**
```yaml
---
description: "Clear description of what this rule covers"
alwaysApply: false
---
```

**Use when:** The rule is contextually relevant but not always needed (e.g., API documentation when working on APIs, multi-agent patterns when building agents).

**Examples:**
- `code-review-and-collaboration` - Code review standards
- `multi-agent-systems` - Multi-agent architecture patterns
- `llm-judge-protocol` - LLM-as-a-Judge evaluation
- `performance-optimization` - Performance best practices

### 3. Apply to Specific Files

Applied when working on files that match the specified glob patterns.

**Frontmatter:**
```yaml
---
globs:
  - "**/api/**/*.py"
  - "**/routes/**/*.py"
alwaysApply: false
---
```

**Use when:** The rule is only relevant for specific file types or locations.

**Examples:**
- `api-documentation-standards` - Applied when working on API files
- `api-interface-and-streaming` - Applied when working on API routes
- `tests-and-validation` - Applied when working on test files
- `langgraph-architecture-and-nodes` - Applied when working on LangGraph nodes

### 4. Apply Manually

Applied only when explicitly mentioned in chat (e.g., `@rule-name`).

**Frontmatter:**
```yaml
---
alwaysApply: false
---
```

**Use when:** The rule is rarely needed and should only be applied on demand (e.g., special audit protocols, meta-rules).

**Note:** Currently, no rules use this type. Meta-rules (`rules-management`, `commands-management`) use "Apply to Specific Files" instead.

## How Rules Are Applied

1. **Always Apply rules** are automatically included in every chat session
2. **Apply Intelligently rules** are considered by the Agent based on the conversation context and the rule's description
3. **Apply to Specific Files rules** are automatically included when you're working on files matching the glob patterns
4. **Apply Manually rules** are only included when you explicitly mention them (e.g., `@rule-name`)

The Agent combines relevant rules to provide comprehensive guidance for your specific task.

## Rule Categories

### Core Rules (`core/`)

Essential rules for all projects:

- **`core-python-standards`** (Always Apply)
  - Python coding standards, best practices, and methodology
  - System planning, code generation, and review processes

- **`error-handling-and-resilience`** (Always Apply)
  - Error handling patterns and resilience strategies
  - Blast radius containment and failure recovery

### Security Rules (`security/`)

Security and governance:

- **`security-governance-and-observability`** (Always Apply)
  - Security standards and governance requirements
  - Security best practices and compliance

- **`audit-protocol`** (Always Apply)
  - Audit procedures and compliance verification
  - Security incident tracking and analysis

### Agent Rules (`agents/`)

Agent-specific architecture:

- **`multi-agent-systems`** (Apply Intelligently)
  - Multi-agent system architecture patterns
  - Orchestrator/Worker/Synthesizer patterns

- **`langgraph-architecture-and-nodes`** (Apply to Specific Files)
  - LangGraph workflow architecture
  - Node structure (READ → DO → WRITE → CONTROL)
  - Applied to LangGraph node files

- **`agentic-logic-and-tools`** (Apply Intelligently)
  - LangChain fundamentals and tool definitions
  - Agent internals and tool implementation

### Infrastructure Rules (`infrastructure/`)

Deployment and operations:

- **`deployment-and-infrastructure`** (Apply Intelligently)
  - CI/CD, Docker, Kubernetes standards
  - Infrastructure deployment patterns

- **`monitoring-and-observability`** (Apply Intelligently)
  - Metrics, logging, tracing standards
  - Observability best practices

- **`performance-optimization`** (Apply Intelligently)
  - Performance optimization strategies
  - Caching, query optimization, resource pooling

- **`multi-tenancy-and-isolation`** (Apply Intelligently)
  - Multi-tenant architecture patterns
  - Data isolation strategies

### Development Rules (`development/`)

Development workflow:

- **`tests-and-validation`** (Apply to Specific Files)
  - Testing framework standards
  - Validation requirements
  - Applied to test files

- **`code-review-and-collaboration`** (Apply Intelligently)
  - Code review standards
  - Git workflow and collaboration practices

- **`versioning-and-release-management`** (Apply Intelligently)
  - Semantic versioning standards
  - Changelog and release management

### API Rules (`api/`)

API development:

- **`api-interface-and-streaming`** (Apply to Specific Files)
  - API design and interface standards
  - Streaming patterns
  - Applied to API route files

- **`api-documentation-standards`** (Apply to Specific Files)
  - OpenAPI/Swagger specifications
  - API documentation requirements
  - Applied to API files

### Data Rules (`data/`)

Data management:

- **`data-schemas-and-interfaces`** (Apply Intelligently)
  - Pydantic schemas and data models
  - Structured interfaces and validation

- **`data-migration-and-compatibility`** (Apply to Specific Files)
  - Data migration patterns
  - Compatibility and versioning strategies
  - Applied to migration files

### Evaluation Rules (`evaluation/`)

LLM evaluation and testing:

- **`llm-evaluation-and-metrics`** (Apply to Specific Files)
  - LLM evaluation frameworks
  - Metrics and scoring standards
  - Applied to evaluation files

- **`llm-judge-protocol`** (Apply Intelligently)
  - LLM-as-a-Judge evaluation protocol
  - Performance, safety, and logic analysis

- **`final-review-protocol`** (Always Apply)
  - Final review process before commit
  - Compliance verification

### Configuration Rules (`configuration/`)

Configuration and setup:

- **`configuration-and-dependency-injection`** (Apply Intelligently)
  - Configuration management using pydantic-settings
  - Dependency injection patterns

- **`prompt-engineering-and-management`** (Apply to Specific Files)
  - Prompt engineering standards
  - Prompt management and versioning
  - Applied to prompt files

### Meta-Rules

Rules for managing rules and commands:

- **`rules-management`** (Apply to Specific Files)
  - Format and structure for creating/updating Rules
  - Applied when working on `RULE.md` files

- **`commands-management`** (Apply to Specific Files)
  - Format and structure for creating/updating Commands
  - Applied when working on command files

## Usage

### Copying Rules to Your Project

#### Option 1: Copy Everything
Copy the entire `.cursor/rules` folder to your project root. Cursor will automatically:
- Apply "Always Apply" rules to every session
- Apply "Apply to Specific Files" rules when working on matching files
- Consider "Apply Intelligently" rules based on context

#### Option 2: Copy by Category
Copy only the category folders you need:

**For all projects:**
- `core/` - Essential coding standards
- `security/` - Security and governance

**For agent projects:**
- `agents/` - Multi-agent patterns
- `evaluation/` - LLM evaluation

**For API projects:**
- `api/` - API design and documentation

**For production projects:**
- `infrastructure/` - Deployment and monitoring

### Rule Application Examples

**Example 1: Working on API code**
- `core-python-standards` (Always Apply) - Active
- `error-handling-and-resilience` (Always Apply) - Active
- `api-interface-and-streaming` (Apply to Specific Files) - Active (matches `**/api/**/*.py`)
- `api-documentation-standards` (Apply to Specific Files) - Active (matches `**/api/**/*.py`)

**Example 2: Working on test files**
- `core-python-standards` (Always Apply) - Active
- `error-handling-and-resilience` (Always Apply) - Active
- `tests-and-validation` (Apply to Specific Files) - Active (matches test files)

**Example 3: Building a multi-agent system**
- `core-python-standards` (Always Apply) - Active
- `error-handling-and-resilience` (Always Apply) - Active
- `multi-agent-systems` (Apply Intelligently) - Considered (relevant to conversation)
- `langgraph-architecture-and-nodes` (Apply to Specific Files) - Active (if working on node files)

## Creating and Updating Rules

When creating or updating Rules, follow the format defined in `.cursor/rules/rules-management/RULE.md`:

1. **Choose the appropriate category** folder
2. **Create the folder structure**: `category-name/rule-name/RULE.md`
3. **Write the frontmatter** based on the rule type:
   - Always Apply: `alwaysApply: true`
   - Apply Intelligently: `description: "..."` and `alwaysApply: false`
   - Apply to Specific Files: `globs: [...]` and `alwaysApply: false`
   - Apply Manually: `alwaysApply: false` (no description or globs)
4. **Write the rule content** following the structure and format guidelines

See `.cursor/rules/rules-management/RULE.md` for detailed format specifications and examples.

## Rule File Format

Every `RULE.md` file must follow this structure:

1. **Frontmatter** (YAML between `---` markers)
   - Defines rule type and application behavior
   - Must be at the very start of the file

2. **Rule Content** (Markdown)
   - Mandate/Overview section
   - Detailed guidelines and standards
   - Examples and best practices

See `.cursor/rules/rules-management/RULE.md` for complete format specifications.

## Integration with Commands

Rules work together with Commands (`.cursor/commands/`) to provide comprehensive workflows:

- **Rules** define standards and patterns that guide the AI's behavior
- **Commands** define workflows that use these standards
- Commands reference Rules in their "Rules Applied" section
- The Agent automatically applies relevant Rules when executing Commands

For example, the `/testing/run-test-suite` command references `tests-and-validation` and `core-python-standards` rules. When you run the command, the Agent automatically applies these rules (if they match the rule type criteria).

## Best Practices

1. **Use Appropriate Rule Types**: Choose the right type based on when the rule should be active
2. **Keep Rules Focused**: Each rule should cover a specific domain or concern
3. **Use Clear Descriptions**: For "Apply Intelligently" rules, write clear, specific descriptions
4. **Use Specific Glob Patterns**: For "Apply to Specific Files" rules, use precise glob patterns
5. **Update Rules Regularly**: Keep rules updated as standards and requirements evolve
6. **Test Rule Application**: Verify that rules are applied correctly in different contexts

## Related Documentation

- **[Root README](../README.md)** - Overview of the entire repository
- **[Commands Documentation](../commands/README.md)** - Complete guide to Cursor Commands
- **[Rules Management Rule](rules-management/RULE.md)** - Format specifications for creating/updating rules
- **[Commands Management Rule](commands-management/RULE.md)** - Format specifications for creating/updating commands
- **[Cursor Rules Documentation](https://cursor.com/docs/context/rules)** - Official Cursor documentation
- **[Cursor Commands Documentation](https://cursor.com/docs/agent/chat/commands)** - Official Cursor documentation
