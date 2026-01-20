---
description: "Standards for configuration management using pydantic-settings and dependency injection patterns"
alwaysApply: false
---

## 1. Pydantic Settings

* **Mandate:** Use **`pydantic-settings`** for all application configuration.

* **Environment Variables:** Never hardcode API keys, model names, or paths. All must come from `.env` files via the Settings class.

* **Validation:** Use Pydantic validators to ensure config values are sane at startup (e.g., verify API key format, check if a path exists).


## 2. Dependency Injection (DI)

* **Pattern:** Pass dependencies (clients, database connections, config objects) into functions/classes rather than instantiating them inside.

* **Benefits:** This makes unit testing easier (mocking is trivial) and decouples logic from infrastructure.

* **Singleton:** Use the Singleton pattern strictly for heavy clients (like `OpenAIClient` or `DatabaseEngine`) to avoid creating new connections per request.


## 3. Secrets Management

* **No Leaks:** Never print config objects to logs without masking sensitive fields (using Pydantic's `SecretStr`).
