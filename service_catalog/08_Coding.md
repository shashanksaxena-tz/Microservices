# DevOps & Coding Services (351-400)

This catalog details AI-native microservices focused on Software Development, Operations, and Engineering.

## 351. Prompt Optimizer
* **Description**: Rewrites user prompts to be more effective for Large Language Models (LLMs), using techniques like Chain-of-Thought (CoT) and few-shot prompting.
* **Features**:
  * Model-specific optimization (GPT-4 vs Claude).
  * "Compression" mode to save tokens.
  * Safety injection.
* **Requirements**:
  * **Models**: Meta-prompting LLM.
* **UI Flow**:
  1. Input: "Write code for a game."
  2. Output: "Act as a senior Python developer. Write a complete Snake game using Pygame..."

## 352. Prompt Version Manager
* **Description**: A registry to track, version, and evaluate prompts used in production.
* **Features**:
  * Diff view between versions.
  * A/B test result tracking.
  * Variable injection syntax `{{var}}`.
* **Requirements**:
  * **Database**: Postgres/Git-based storage.
* **UI Flow**:
  1. Dashboard listing prompts.
  2. Click "v2.1" to see changes vs "v2.0".
  3. "Deploy v2.1" button.

## 353. Cost Estimator (LLM)
* **Description**: Estimates the cost of an API call or batch job before execution.
* **Features**:
  * Token counting (Tiktoken).
  * Price lookup (OpenAI/Anthropic/Azure).
* **Requirements**:
  * **Logic**: Tokenizer + Pricing Table.
* **UI Flow**:
  1. Paste text/prompt.
  2. "Tokens: 500. Cost: $0.015".

## 354. Drift Detector
* **Description**: Monitors input/output data distributions to detect when a model is becoming stale (Data Drift / Concept Drift).
* **Features**:
  * KS-test / PSI score.
  * Alerting via Slack/PagerDuty.
* **Requirements**:
  * **Models**: Statistical profiling.
* **UI Flow**:
  1. Dashboard graph.
  2. Red spike: "Input distribution changed significantly today."

## 355. Model Router
* **Description**: Dynamically routes queries to the most appropriate model based on difficulty, cost, or latency requirements.
* **Features**:
  * "Cascading" (Try cheap model -> fallback to expensive).
  * Latency-based routing.
* **Requirements**:
  * **Logic**: Classifier / Router Gateway.
* **UI Flow**:
  1. API Gateway Config.
  2. "Route: Simple queries -> Llama 7B, Complex -> GPT-4".

## 356. Latency Analyzer
* **Description**: Traces and analyzes the latency of AI chains to find bottlenecks.
* **Features**:
  * Span visualization (Waterfall).
  * TTFT (Time to First Token) tracking.
* **Requirements**:
  * **Infrastructure**: OpenTelemetry.
* **UI Flow**:
  1. Trace view.
  2. "Bottleneck: Vector DB lookup took 2s."

## 357. Code Reviewer
* **Description**: Automated code review bot that comments on Pull Requests with stylistic and functional feedback.
* **Features**:
  * Security check.
  * Convention enforcement.
  * "LGTM" scoring.
* **Requirements**:
  * **Models**: CodeLlama / GPT-4.
* **UI Flow**:
  1. GitHub Action triggers.
  2. Bot comments on lines of code in PR.

## 358. Git Commit Message Generator
* **Description**: Analyzes staged changes (diffs) and generates a semantic commit message.
* **Features**:
  * Conventional Commits format (`feat:`, `fix:`).
  * Bullet point summaries.
* **Requirements**:
  * **Models**: Code-LLM.
* **UI Flow**:
  1. CLI command `git-ai-commit`.
  2. Suggestion: `fix: handle null pointer in auth service`.

## 359. Release Note Generator
* **Description**: Compiles a changelog from a list of commit messages or PR titles.
* **Features**:
  * Categorization (Features, Bug Fixes).
  * "Marketing speak" translation.
* **Requirements**:
  * **Models**: Summarization.
* **UI Flow**:
  1. Select tag range (v1.0 -> v1.1).
  2. Markdown Release Notes generated.

## 360. Documentation Updater
* **Description**: Detects when code changes make documentation obsolete and suggests updates.
* **Features**:
  * Docstring sync.
  * README update suggestions.
* **Requirements**:
  * **Models**: Code-text alignment.
* **UI Flow**:
  1. CI pipeline failure: "Doc out of sync".
  2. PR created with doc updates.

## 361. StackOverflow Answer Summarizer
* **Description**: Summarizes answers from StackOverflow threads to solve a specific error.
* **Features**:
  * "Accepted Answer" extraction.
  * Code snippet consolidation.
* **Requirements**:
  * **Models**: RAG over web results.
* **UI Flow**:
  1. Paste Error.
  2. "Try running `npm install` (Source: SO thread 123)".

## 362. Error Log Analyzer
* **Description**: Clusters and analyzes server logs to identify root causes of spikes.
* **Features**:
  * Pattern recognition.
  * Anomaly detection.
* **Requirements**:
  * **Models**: Clustering (DBSCAN).
* **UI Flow**:
  1. Kibana/Log view.
  2. "Cluster 5: Database Timeout (5000 occurrences)".

## 363. Security Vulnerability Scanner (SAST)
* **Description**: Scans source code for security flaws (SQLi, XSS, Hardcoded secrets).
* **Features**:
  * False positive filtering (using AI understanding).
  * Fix suggestion.
* **Requirements**:
  * **Models**: Security-tuned Code model.
* **UI Flow**:
  1. Upload zip.
  2. "Critical: API Key found in `config.py`".

## 364. Phishing Detector
* **Description**: Analyzes emails or URLs to detect phishing attempts.
* **Features**:
  * Homograph attack detection.
  * Urgency language detection.
* **Requirements**:
  * **Models**: Classification.
* **UI Flow**:
  1. Browser extension.
  2. Warning overlay: "Suspected Phishing Site".

## 365. Spam Filter
* **Description**: Filters user-generated content (comments, reviews) for spam.
* **Features**:
  * Context-aware (not just keyword).
  * "Crypto scam" detection.
* **Requirements**:
  * **Models**: Classification.
* **UI Flow**:
  1. API `is_spam("Buy cheap rolex")` -> `True`.

## 366. Unit Test Generator
* **Description**: Writes unit tests for a given function or class.
* **Features**:
  * Framework selection (Pytest, Jest).
  * Edge case coverage.
* **Requirements**:
  * **Models**: Code-LLM.
* **UI Flow**:
  1. Highlight function.
  2. "Generate Tests".
  3. `test_func.py` created.

## 367. Integration Test Generator
* **Description**: Generates end-to-end (E2E) test scripts based on user flows.
* **Features**:
  * Playwright/Cypress code gen.
  * Natural language to test script.
* **Requirements**:
  * **Models**: Code-LLM.
* **UI Flow**:
  1. "Test login flow".
  2. Playwright script generated.

## 368. API Mock Generator
* **Description**: Creates a mock server implementation from an OpenAPI/Swagger spec.
* **Features**:
  * Realistic data generation (Faker).
  * Latency simulation.
* **Requirements**:
  * **Models**: Schema parsing.
* **UI Flow**:
  1. Upload `openapi.yaml`.
  2. Get Docker container with mock server.

## 369. Environment Variable Manager
* **Description**: Scans code to find required environment variables and generates a `.env.example`.
* **Features**:
  * Default value suggestion.
  * Secret detection.
* **Requirements**:
  * **Models**: AST parsing / Regex.
* **UI Flow**:
  1. `scan .`
  2. `.env.example` generated.

## 370. Dependency Updater
* **Description**: Checks for outdated dependencies and assesses breaking changes using AI summary of changelogs.
* **Features**:
  * "Safe update" probability.
  * Migration guide summary.
* **Requirements**:
  * **Models**: NLP.
* **UI Flow**:
  1. "Update React to v18?"
  2. "Risk: High (Breaking changes in X)".

## 371. Refactoring Agent
* **Description**: Autonomously refactors code to improve maintainability or performance.
* **Features**:
  * "Extract Method".
  * "Convert to Async".
* **Requirements**:
  * **Models**: Code-LLM.
* **UI Flow**:
  1. Select code block.
  2. "Refactor".
  3. Diff view of improvements.

## 372. SQL Query Optimizer
* **Description**: Rewrites SQL queries to be more efficient.
* **Features**:
  * Index usage explanation.
  * N+1 problem detection.
* **Requirements**:
  * **Models**: SQL-tuned model.
* **UI Flow**:
  1. Paste Query.
  2. Optimized Query + Explanation.

## 373. Regex Explainer
* **Description**: Explains what a complex Regular Expression does in plain English.
* **Features**:
  * Visual breakdown.
* **Requirements**:
  * **Models**: Code-LLM.
* **UI Flow**:
  1. Paste Regex.
  2. "Matches an email address..."

## 374. JSON-to-TS Interface Generator
* **Description**: Converts a JSON object into a TypeScript interface or Pydantic model.
* **Features**:
  * Type inference.
  * Nested structure handling.
* **Requirements**:
  * **Models**: Deterministic parsing.
* **UI Flow**:
  1. Paste JSON response.
  2. Copy TypeScript Interface.

## 375. Kubernetes Manifest Generator
* **Description**: Generates K8s YAML (Deployment, Service, Ingress) from a simple description.
* **Features**:
  * Best practice defaults.
* **Requirements**:
  * **Models**: Infrastructure-tuned LLM.
* **UI Flow**:
  1. "Deploy nginx on port 80 with 3 replicas."
  2. YAML generated.

## 376. Dockerfile Generator
* **Description**: Generates an optimized Dockerfile for a project.
* **Features**:
  * Multi-stage build support.
  * Language detection.
* **Requirements**:
  * **Models**: Dev-tuned LLM.
* **UI Flow**:
  1. Scan repo.
  2. `Dockerfile` created.

## 377. Code Translation Service
* **Description**: Translates code from one language to another (e.g., Java to Kotlin, Python to Go).
* **Features**:
  * Idiomatic translation.
  * Library mapping.
* **Requirements**:
  * **Models**: Code-LLM.
* **UI Flow**:
  1. Paste Java code.
  2. Select "Go".
  3. Output Go code.

## 378. Variable Naming Assistant
* **Description**: Suggests descriptive variable and function names.
* **Features**:
  * Context awareness.
  * Convention (camelCase/snake_case) support.
* **Requirements**:
  * **Models**: Code-LLM.
* **UI Flow**:
  1. Highlight `var x = ...`
  2. Suggestion: `userRegistrationTimestamp`.

## 379. Technical Debt Estimator
* **Description**: Analyzes codebase to estimate "Technical Debt" in hours/dollars.
* **Features**:
  * TODO comment counting.
  * Complexity metrics (Cyclomatic).
* **Requirements**:
  * **Models**: Static Analysis + ML.
* **UI Flow**:
  1. Dashboard.
  2. "Tech Debt: 400 hours".

## 380. License Compliance Checker
* **Description**: Scans dependencies to ensure license compatibility (e.g., no GPL in commercial).
* **Features**:
  * Dependency tree traversal.
* **Requirements**:
  * **Data**: License database.
* **UI Flow**:
  1. `npm audit`.
  2. "Error: 'left-pad' is GPL v3".

## 381. API Doc Generator
* **Description**: Generates documentation (Swagger/Markdown) from code comments and signatures.
* **Features**:
  * Example generation.
* **Requirements**:
  * **Models**: Code-LLM.
* **UI Flow**:
  1. Point to `/routes`.
  2. `docs.md` generated.

## 382. GraphQL Schema Generator
* **Description**: Generates GraphQL schema from SQL schema or JSON.
* **Features**:
  * Resolver generation.
* **Requirements**:
  * **Models**: Code-LLM.
* **UI Flow**:
  1. Upload `schema.sql`.
  2. Get `schema.graphql`.

## 383. CSS Class Sorter
* **Description**: Sorts Tailwind classes or CSS properties for consistency.
* **Features**:
  * Logical grouping (Layout, Typography).
* **Requirements**:
  * **Models**: Deterministic / NLP.
* **UI Flow**:
  1. `class="red-500 p-4 flex"`
  2. `class="flex p-4 red-500"`

## 384. Accessibility (A11y) Fixer
* **Description**: Scans HTML/JSX for accessibility issues and suggests fixes.
* **Features**:
  * ARIA role suggestions.
  * Contrast check.
* **Requirements**:
  * **Models**: Code/Vision.
* **UI Flow**:
  1. Scan component.
  2. "Add `aria-label` to button."

## 385. Terraform Generator
* **Description**: Generates Infrastructure-as-Code (Terraform) from architecture descriptions.
* **Features**:
  * AWS/Azure/GCP support.
* **Requirements**:
  * **Models**: IaC-tuned LLM.
* **UI Flow**:
  1. "S3 bucket with public read."
  2. HCL code generated.

## 386. Database Seeder
* **Description**: Generates dummy data SQL scripts to populate a database for testing.
* **Features**:
  * Foreign key consistency.
  * Realistic PII generation.
* **Requirements**:
  * **Models**: Data generation.
* **UI Flow**:
  1. Connect DB.
  2. "Insert 1000 users".

## 387. Cron Expression Generator
* **Description**: Converts "Every Tuesday at 5pm" to Cron syntax.
* **Features**:
  * Explanation of cron strings.
* **Requirements**:
  * **Models**: NLP.
* **UI Flow**:
  1. Input description.
  2. `0 17 * * 2`.

## 388. Log Anonymizer
* **Description**: Strips PII (IPs, Emails) from logs before storage.
* **Features**:
  * Stream processing.
* **Requirements**:
  * **Models**: NER.
* **UI Flow**:
  1. Log Stream -> [Service] -> Safe Log.

## 389. Code Complexity Visualizer
* **Description**: Generates a heatmap of the codebase showing complex/hot files.
* **Features**:
  * Churn vs Complexity graph.
* **Requirements**:
  * **Analysis**: Git + Static analysis.
* **UI Flow**:
  1. View Repo Map.
  2. Red areas = High Complexity.

## 390. Dead Code Detector
* **Description**: Identifies unused functions, variables, and exports.
* **Features**:
  * Call graph analysis.
* **Requirements**:
  * **Analysis**: Static analysis.
* **UI Flow**:
  1. Report: "Function `oldAuth` is never called."

## 391. Semantic Code Search
* **Description**: Searches code by meaning ("auth logic") rather than keyword.
* **Features**:
  * Natural language query.
* **Requirements**:
  * **Models**: Embeddings.
* **UI Flow**:
  1. "Where do we handle login?"
  2. Jumps to `LoginController.ts`.

## 392. CI/CD Pipeline Generator
* **Description**: Generates config for GitHub Actions, GitLab CI, etc.
* **Features**:
  * Build, Test, Deploy steps.
* **Requirements**:
  * **Models**: DevOps LLM.
* **UI Flow**:
  1. "Node.js app on AWS".
  2. `.github/workflows/deploy.yml` generated.

## 393. User Story Generator
* **Description**: Converts a feature idea into structured User Stories with Acceptance Criteria.
* **Features**:
  * Gherkin syntax support.
* **Requirements**:
  * **Models**: PM-tuned LLM.
* **UI Flow**:
  1. "Add Dark Mode".
  2. "As a user, I want..."

## 394. QA Scenario Generator
* **Description**: Generates a list of manual test cases for a feature.
* **Features**:
  * Positive/Negative paths.
* **Requirements**:
  * **Models**: QA-tuned LLM.
* **UI Flow**:
  1. "Login Page".
  2. "Test 1: Valid credentials..."

## 395. App Store Description Optimizer
* **Description**: Optimizes App Store/Play Store descriptions for ASO.
* **Features**:
  * Keyword density.
* **Requirements**:
  * **Models**: Marketing NLP.
* **UI Flow**:
  1. Paste description.
  2. Optimized version.

## 396. Browser Extension Generator
* **Description**: Scaffolds a browser extension (manifest, background script).
* **Features**:
  * Chrome/Firefox support.
* **Requirements**:
  * **Models**: Code Gen.
* **UI Flow**:
  1. "Popup that shows weather."
  2. Download Zip.

## 397. Favicon Generator
* **Description**: Generates a favicon from a text description or image.
* **Features**:
  * ICO/PNG export.
* **Requirements**:
  * **Models**: Image Gen.
* **UI Flow**:
  1. "Blue Rocket".
  2. Download `favicon.ico`.

## 398. Color Blindness Simulator
* **Description**: Simulates how a UI looks to users with different color blindness types.
* **Features**:
  * Protanopia, Deuteranopia filters.
* **Requirements**:
  * **Models**: Image processing.
* **UI Flow**:
  1. Upload screenshot.
  2. View as "Deuteranopia".

## 399. Text Texture Generator
* **Description**: Generates seamless textures for 3D models from text.
* **Features**:
  * Normal/Bump map generation.
* **Requirements**:
  * **Models**: Texture synthesis.
* **UI Flow**:
  1. "Rusty Metal".
  2. Download Texture maps.

## 400. 3D Model Generator (Text-to-3D)
* **Description**: Generates simple 3D assets (GLB/OBJ) from text prompts.
* **Features**:
  * Low-poly / Voxel styles.
* **Requirements**:
  * **Models**: Point-E / Shap-E.
* **UI Flow**:
  1. "A red chair".
  2. View and download 3D model.
