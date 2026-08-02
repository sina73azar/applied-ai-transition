# Applied AI Systems Engineer Roadmap

## Target

Transition from Senior Android Engineer to Applied AI Systems Engineer while
preserving senior-level strengths in architecture, performance, security,
tooling, and mobile engineering.

Primary roles:

1. Applied AI Engineer / AI Systems Engineer
2. Backend Engineer for AI products
3. AI Platform or Developer Productivity Engineer
4. Mobile / On-device AI Engineer

Initial hiring priority is Iran. International remote roles are the second
market after the public portfolio and English case studies are ready.

## Timeline and Gates

| Dates | Focus | Required evidence | Exit gate |
|---|---|---|---|
| Aug-Sep 2026 | Independent Python ownership | Completed foundation checks and FastAPI capstone | Build and debug a typed API feature without generated code |
| Oct-Nov 2026 | Practical ML foundations | Ticket-intelligence project with reproducible experiments | Defend data split, metric, baseline, and error analysis |
| Dec 2026-Feb 2027 | LLM and retrieval systems | Public RAG evaluation harness and benchmark report | Prove an improvement with retrieval and answer metrics |
| Mar-May 2027 | Production AI and Android differentiator | Observable deployment and hybrid Android/AI demo | Operate, load-test, and recover the system |
| Jun-Jul 2027 | Interviews and applications | Two flagship projects, one ML project, three case studies | Consistently pass representative mock interviews |
| Aug 2027-Jul 2028 | Role-driven specialization | Work or interview evidence identifies the next gap | Choose AI platform, on-device AI, or deeper ML |

Do not advance because a date has passed. Advance when the exit gate is met.

## Phase 1: Python Ownership

Follow [python_foundations/README.md](python_foundations/README.md). The final
capstone is a separate Support Operations API built from a blank directory.

Required capstone behavior:

- typed FastAPI endpoints for tickets, comments, status changes, and search;
- Pydantic request and response models;
- PostgreSQL persistence and a documented schema migration;
- authentication, pagination, consistent errors, and input validation;
- one background operation with explicit retry behavior;
- unit and API tests, including authorization and failure cases;
- structured logging and a health endpoint;
- Docker Compose startup and a concise architecture note.

Python exit interview:

- implement one new endpoint and its tests in 90 minutes;
- explain async execution, dependency injection, exceptions, typing, and
  transaction boundaries;
- diagnose one injected test failure without an AI assistant.

## Phase 2: Practical Machine Learning

Use the free scikit-learn MOOC as the main sequence:
<https://inria.github.io/scikit-learn-mooc/>.

Study NumPy, pandas, SQL analysis, train/validation/test separation,
cross-validation, leakage, classification, regression, tree ensembles,
clustering, pipelines, class imbalance, calibration, and error analysis.
Learn the practical meaning of probability, distributions, vectors, matrices,
gradients, and optimization.

Build a Support Ticket Intelligence service with open or synthetic data:

- predict category and priority;
- retrieve likely duplicate tickets;
- establish keyword and majority-class baselines;
- keep data preparation and experiment runs reproducible;
- report per-class precision/recall/F1, confusion matrix, calibration, latency,
  and failure slices;
- expose the selected model through a tested, containerized API;
- publish a model card and a short English case study.

Exit interview:

- justify the split strategy and metrics;
- identify leakage and imbalance risks;
- explain why the selected model beats the baseline;
- describe the most important remaining error category.

## Phase 3: LLM and Retrieval Engineering

Use Full Stack Deep Learning for lifecycle concepts:
<https://fullstackdeeplearning.com/>.

Study tokenization, transformer behavior, embeddings, dense and sparse
retrieval, rank fusion, reranking, structured outputs, bounded tool use, prompt
injection, isolation, permissions, and offline evaluation.

Turn the existing RAG prototype into a public evaluation case study:

- use licensed open-source repositories, public documentation, and synthetic
  Jira/environment/deployment records;
- remove company-specific sample data and never publish a Qdrant snapshot made
  from internal sources;
- create a versioned evaluation dataset containing expected evidence, required
  facts, forbidden claims, and refusal cases;
- measure recall@k, MRR, citation precision, grounded-answer rate, refusal
  correctness, p50/p95 latency, and resource usage;
- compare lexical-only, dense-only, and hybrid retrieval;
- publish a benchmark report including negative or inconclusive results;
- identify precisely which design and implementation work is personally owned.

Use an agent framework only after implementing one small tool loop and its
state/error handling directly in Python.

## Phase 4: Production AI Engineering

Extend the evaluated system with:

- PostgreSQL application state and queued ingestion work;
- idempotency, retry limits, and dead-letter handling;
- configuration validation, secret handling, and CI;
- OpenTelemetry traces, metrics, structured logs, and a dashboard;
- rate limiting, audit events, and project/tenant isolation;
- load tests and dependency-failure tests;
- documented backup, migration, rollback, and recovery procedures;
- local model serving and an optional OpenAI-compatible provider.

Kubernetes is deferred until a target role or real deployment requires it.

Build an Android differentiator:

- Kotlin/Compose client with a Python AI backend;
- one privacy-sensitive capability that can run on-device;
- explicit local/server fallback behavior;
- latency, memory, battery, offline, and unsupported-device measurements;
- a design note explaining privacy and placement decisions.

## Phase 5: Portfolio and Job Search

Start tracking roles and networking in January 2027. Begin selective
applications in April 2027 and the main campaign in June 2027.

Public portfolio requirements:

- evaluated RAG system;
- Android/AI hybrid system;
- smaller classical-ML system;
- reproducible setup, architecture diagram, short demo, metrics, and limitations
  for each flagship;
- three English case studies using
  [PORTFOLIO_EVIDENCE.md](PORTFOLIO_EVIDENCE.md).

Interview rotation:

- Python coding and debugging;
- SQL and backend/API design;
- ML metrics, leakage, experiments, and error analysis;
- RAG/AI system design, evaluation, safety, latency, and cost;
- Android/on-device performance and privacy;
- senior behavioral stories about architecture, leadership, and failures.

Present AI assistance honestly: explain the problem personally framed, decisions
personally made, generated portions reviewed, tests added, failures diagnosed,
and measurable outcome.

## Weekly Allocation

| Work | Hours |
|---|---:|
| Python, ML, or LLM study | 3 |
| Portfolio implementation | 4 |
| Tests, evaluation, and documentation | 1 |
| English writing, networking, or interviews | 1 |
| Optional reading or Android experiment | 1 |

Every fourth week is consolidation: finish work, rerun evaluation, remove
fragility, and improve explanations. Do not introduce another framework.

## Long-Term Decision

Review the direction in July 2027:

- choose AI Systems/Platform if reliability and infrastructure are most
  rewarding;
- choose On-device AI if optimization, privacy, and Android integration are
  most rewarding;
- choose deeper ML Engineering only if experimentation and model behavior
  justify more mathematics and training work.

