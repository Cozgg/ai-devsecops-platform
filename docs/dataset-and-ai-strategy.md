# Dataset and AI Strategy

## Goal

This document defines how datasets, RAG, LangChain/LangGraph, and AI Agents should be used in the AI DevSecOps Platform.

The project should not try to train a large language model from scratch during the MVP phase. Instead, it should use existing scanner tools, public datasets for evaluation/demo, lightweight anomaly detection algorithms, and RAG-based AI Agents for explanation and remediation.

## Recommended approach

```text
Scanner tools detect issues
→ Normalizer converts outputs to common finding schema
→ Risk scoring ranks issues
→ RAG retrieves relevant security knowledge
→ AI Code Agent explains risks and suggests fixes
```

For DevOps monitoring:

```text
System logs/metrics are collected
→ Rule-based or lightweight ML anomaly detector finds suspicious behavior
→ Incident is created
→ AI DevOps Agent reads logs/metrics and suggests basic actions
```

## Should we use RAG, LangChain, or LangGraph?

Use all of them, but with different roles:

- RAG is the architecture for retrieving relevant knowledge before asking the LLM to answer.
- LangChain can be used to build retrievers, prompt templates, tools, and chains.
- LangGraph is better when the AI Agent has multiple steps, state, retry logic, or tool-calling workflow.

Recommended MVP:

```text
RAG + LangChain for AI Code Analysis Agent
Simple tool-calling or LangGraph for AI DevOps Agent
PostgreSQL + pgvector for vector storage
```

Recommended thesis extension:

```text
LangGraph multi-step agent
GraphRAG for vulnerability / file / function / CWE / fix-pattern relationships
Observability-aware AI DevOps Agent
Human approval before any automated remediation
```

## Dataset groups

### 1. Source code vulnerability datasets

Purpose:

- Test source code risk detection.
- Evaluate scanner and AI report quality.
- Build a small vulnerability knowledge base.
- Optionally train a lightweight classifier later.

Recommended datasets:

- NIST SARD / Juliet Test Suite
- Devign
- DiverseVul
- Big-Vul
- MegaVul
- CVEfixes
- Small custom vulnerable sample projects created for this project

MVP recommendation:

Use custom vulnerable projects + Semgrep/Trivy/Bandit output first. Do not fine-tune a model yet.

### 2. Log analysis datasets

Purpose:

- Test log parsing.
- Test anomaly detection.
- Evaluate AI DevOps Agent incident summaries.

Recommended datasets:

- LogHub: HDFS, BGL, OpenStack, Hadoop and other system logs
- Numenta Anomaly Benchmark for streaming time-series anomaly detection
- Self-generated logs from backend, worker, scanner, and queue failures

MVP recommendation:

Use self-generated logs + selected LogHub samples. Start with rule-based detection.

### 3. System metrics and anomaly datasets

Purpose:

- Test system health anomaly detection.
- Simulate CPU, memory, latency, error rate, and queue backlog changes.

Recommended datasets:

- Numenta Anomaly Benchmark
- Skoltech Anomaly Benchmark
- Synthetic metrics generated from local Docker Compose services

MVP recommendation:

Generate your own metrics first. Add NAB/SKAB for evaluation later.

### 4. RAG knowledge base data

Purpose:

- Ground AI explanations and remediation suggestions.
- Reduce hallucination.
- Provide citations/references in reports.

Recommended sources:

- OWASP Top 10 notes
- CWE descriptions
- NVD/CVE descriptions
- Semgrep rule docs
- Trivy vulnerability output
- Secure coding examples created by the project
- Internal runbooks for scanner failures, queue backlog, worker timeout, and API error spikes

## MVP dataset plan

### Phase 1: Demo and scanner validation

Create local sample projects:

```text
samples/vulnerable-node-app
samples/vulnerable-python-app
samples/secure-node-app
```

Include these vulnerability cases:

```text
SQL Injection
Hardcoded Secret
Insecure CORS
Weak JWT secret
Command Injection
Missing input validation
Vulnerable dependency
Debug mode enabled
```

### Phase 2: RAG knowledge base

Create markdown documents:

```text
knowledge_base/sql_injection.md
knowledge_base/hardcoded_secret.md
knowledge_base/insecure_cors.md
knowledge_base/weak_jwt_secret.md
knowledge_base/dependency_vulnerability.md
knowledge_base/queue_backlog_runbook.md
knowledge_base/scanner_failure_runbook.md
knowledge_base/api_error_spike_runbook.md
```

### Phase 3: Log/anomaly evaluation

Use:

```text
self-generated backend logs
self-generated worker logs
self-generated scanner failure logs
selected LogHub logs
selected NAB time-series files
```

## Training strategy

For the MVP, do not train a large model.

Recommended MVP strategy:

```text
Semgrep / Trivy / Bandit for actual detection
Rule-based anomaly detection for system health
RAG + LLM for explanation and remediation
```

Optional lightweight ML:

```text
Isolation Forest for metrics anomaly detection
Z-score or moving average for latency/error-rate anomaly
Simple classifier for scanner finding prioritization
```

Future thesis strategy:

```text
Fine-tune small code model for vulnerability classification
Evaluate on Devign / DiverseVul / Big-Vul / MegaVul
Compare scanner-only vs scanner + AI/RAG explanations
Implement GraphRAG for vulnerability knowledge reasoning
```

## Decision

For this project:

```text
Use RAG as the core AI architecture.
Use LangChain for RAG pipeline and tool wrappers.
Use LangGraph later if the AI Agent needs multi-step reasoning and stateful workflows.
Do not train LLM from scratch in the MVP.
Use datasets mainly for testing, evaluation, and small anomaly models.
```
