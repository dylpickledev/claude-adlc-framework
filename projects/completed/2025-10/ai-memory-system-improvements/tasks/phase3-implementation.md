# Phase 3 Implementation Plan: Semantic Search
## Weeks 5-6 (Target: 2-3 days accelerated)

**Goal**: Enable intelligent "have we seen this before?" pattern discovery using semantic similarity.

**Success Criteria**:
- ✅ >85% semantic search accuracy
- ✅ <200ms query response time
- ✅ Pattern recommendation from user queries
- ✅ Integration with Phase 1 budget system
- ✅ Zero additional cloud dependencies

---

## Overview

### The Problem

**Current State** (Phase 1 + 2):
- Token-aware loading based on metadata (recency, usage, confidence)
- Context matching uses keyword search (agent name, technology tags)
- No semantic understanding of pattern content
- Can't answer "have we solved something similar?"

**User Pain Points**:
- "I think we did something like this before..." → manual search required
- Similar problems with different terminology → not found
- Related patterns not surfaced → reinventing solutions

### The Solution

**Semantic Search Architecture**:
1. **Vector Embeddings**: Convert patterns to dense vectors (768-dim)
2. **Local Vector Store**: ChromaDB for fast similarity search
3. **Hybrid Retrieval**: Combine semantic + metadata scoring
4. **Pattern Recommendations**: Suggest related patterns for current task

**Key Design Decisions**:
- **Model**: `sentence-transformers/all-MiniLM-L6-v2` (lightweight, fast, accurate)
- **Vector DB**: ChromaDB (local, no cloud, privacy-preserving)
- **Embedding Strategy**: Full pattern content + metadata
- **Query Types**: Natural language, task descriptions, problem statements

---

## Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Phase 3: Semantic Search                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐      ┌─────────────────────┐         │
│  │  Pattern Files   │──────│ Embedding Generator │         │
│  │  (.md + .json)   │      │  (sentence-trans)   │         │
│  └──────────────────┘      └─────────────────────┘         │
│           │                          │                       │
│           │                          ▼                       │
│           │                 ┌─────────────────┐            │
│           │                 │  Vector Store   │            │
│           │                 │   (ChromaDB)    │            │
│           │                 └─────────────────┘            │
│           │                          │                       │
│           ▼                          │                       │
│  ┌──────────────────┐               │                       │
│  │  Metadata Store  │               │                       │
│  │ (token counts,   │               │                       │
│  │  usage, etc)     │               │                       │
│  └──────────────────┘               │                       │
│           │                          │                       │
│           └──────────┬───────────────┘                       │
│                      │                                       │
│                      ▼                                       │
│           ┌─────────────────────┐                           │
│           │  Hybrid Retrieval   │                           │
│           │ (semantic + metadata)│                          │
│           └─────────────────────┘                           │
│                      │                                       │
│                      ▼                                       │
│           ┌─────────────────────┐                           │
│           │ Pattern Recommender │                           │
│           │  (ranked results)   │                           │
│           └─────────────────────┘                           │
│                                                               │
└─────────────────────────────────────────────────────────────┘

Integration with Phase 1:
  Pattern Recommender → Memory Budget → Load Top-K Patterns
```

### Data Flow

**Embedding Generation** (One-time + incremental):
```
1. Scan pattern files (.claude/memory/**/*.md)
2. Load pattern content + metadata
3. Generate embedding (768-dim vector)
4. Store in ChromaDB with metadata
5. Create embedding cache (.claude/cache/embeddings/)
```

**Semantic Search** (Query time):
```
1. User query: "How do we handle dbt errors?"
2. Generate query embedding (same model)
3. ChromaDB similarity search (cosine similarity)
4. Retrieve top-N candidates (N=20)
5. Re-rank with metadata (recency, usage, confidence)
6. Apply Phase 1 budget constraints
7. Return top-K patterns (K=8)
```

---

## Task Breakdown

### Task 1: Set Up Vector Embedding Infrastructure

**Effort**: 30 minutes

**Dependencies**:
- `sentence-transformers` library
- `chromadb` library
- Virtual environment from Phase 1

**Deliverables**:
1. Update `requirements.txt` with new dependencies
2. Install in project venv
3. Create `.claude/vector-store/` directory
4. Test basic embedding generation

**Script**: `scripts/setup-semantic-search.py`

**Success Criteria**:
- Libraries installed successfully
- Can generate test embedding
- ChromaDB initializes

---

### Task 2: Build Pattern Embedding Generator

**Effort**: 2 hours

**Purpose**: Generate vector embeddings for all patterns.

**Script**: `scripts/generate-embeddings.py`

**Features**:
- Load all patterns from memory directories
- Extract content for embedding (full text + metadata)
- Generate 768-dim embeddings using sentence-transformers
- Store in ChromaDB with metadata
- Incremental updates (only embed new/changed patterns)
- Embedding cache for performance

**Embedding Strategy**:
```python
# Combine pattern content with structured metadata
embedding_text = f"""
Title: {pattern_title}
Category: {pattern_category}
Technologies: {', '.join(technologies)}

Problem:
{problem_section}

Solution:
{solution_section}

When to Apply:
{when_to_apply_section}
"""
```

**Metadata Stored with Embedding**:
- `pattern_file`: Path to pattern
- `token_count`: Token count
- `confidence`: Confidence score
- `use_count`: Usage count
- `last_used`: Last used timestamp
- `created_at`: Creation timestamp
- `embedding_generated_at`: When embedded

**CLI**:
```bash
# Generate embeddings for all patterns
python scripts/generate-embeddings.py

# Update embeddings for changed patterns only
python scripts/generate-embeddings.py --incremental

# Force regenerate all embeddings
python scripts/generate-embeddings.py --force

# Generate for specific directory
python scripts/generate-embeddings.py --dir .claude/memory/patterns
```

**Success Criteria**:
- All 55+ patterns embedded
- ChromaDB vector count matches pattern count
- Incremental updates work correctly
- <1 second per pattern embedding time

---

### Task 3: Implement Semantic Similarity Search

**Effort**: 2 hours

**Purpose**: Query patterns using natural language.

**Script**: `scripts/semantic-search.py`

**Features**:
- Natural language query input
- Query embedding generation
- Cosine similarity search in ChromaDB
- Hybrid scoring (semantic + metadata)
- Result ranking and filtering

**Hybrid Scoring Algorithm**:
```python
final_score = (
    semantic_similarity * 0.60 +  # Primary: semantic match
    recency_score * 0.15 +         # Secondary: recent patterns
    usage_score * 0.15 +           # Secondary: proven patterns
    confidence_score * 0.10        # Tertiary: validated patterns
)
```

**Query Types Supported**:
1. **Problem Query**: "How do we handle dbt errors?"
2. **Task Query**: "Need to create a Snowflake view"
3. **Technology Query**: "Tableau dashboard performance"
4. **Similarity Query**: "Similar to auth-patterns.md"

**CLI**:
```bash
# Search patterns semantically
python scripts/semantic-search.py "How do we handle dbt errors?"

# Show top 10 results
python scripts/semantic-search.py "Snowflake optimization" --top 10

# Explain scoring
python scripts/semantic-search.py "React patterns" --explain

# Filter by technology
python scripts/semantic-search.py "dashboard patterns" --tech tableau
```

**Output Format**:
```
🔍 Semantic Search Results for: "How do we handle dbt errors?"
─────────────────────────────────────────────────────────────
Rank 1: dbt-error-patterns.md (Score: 0.89)
  Semantic:   0.92 (high match)
  Recency:    0.85 (7 days ago)
  Usage:      0.90 (5 uses)
  Confidence: 0.88

  Snippet: "Pattern for handling dbt compilation and runtime errors..."

Rank 2: error-handling-best-practices.md (Score: 0.81)
  ...
```

**Success Criteria**:
- Query response time <200ms
- Relevant patterns ranked highly
- Irrelevant patterns filtered out
- Hybrid scoring balances semantic + metadata

---

### Task 4: Create Pattern Recommendation Engine

**Effort**: 1.5 hours

**Purpose**: Automatically suggest patterns based on current task context.

**Script**: `scripts/recommend-patterns.py`

**Features**:
- Context-aware recommendations
- Multi-query recommendation (batch queries)
- Related pattern discovery
- Diversity in recommendations (avoid redundancy)

**Recommendation Strategies**:

1. **Task-Based**: Given current task description → recommend patterns
2. **Pattern-Based**: Given one pattern → recommend related patterns
3. **Problem-Based**: Given problem statement → recommend solutions
4. **Agent-Based**: Given agent role → recommend domain patterns

**CLI**:
```bash
# Recommend patterns for task
python scripts/recommend-patterns.py --task "Create a Tableau dashboard"

# Recommend related patterns
python scripts/recommend-patterns.py --similar dbt-best-practices.md

# Recommend for agent
python scripts/recommend-patterns.py --agent analytics-engineer-role

# Top 5 recommendations with reasons
python scripts/recommend-patterns.py --task "Fix Snowflake query" --top 5 --explain
```

**Integration with Phase 1**:
```python
# Get recommendations
recommendations = recommender.recommend(
    task="Create Tableau dashboard",
    agent="bi-developer-role",
    top_n=20  # Get more candidates
)

# Apply Phase 1 budget constraints
memory_budget = MemoryBudget(max_tokens=20000)
loaded_patterns = memory_budget.load_patterns_with_budget(
    recommendations  # Already ranked by hybrid score
)

# Result: Top-K patterns within budget
```

**Success Criteria**:
- Recommendations relevant to task
- Diversity in recommended patterns
- Fast recommendation generation (<300ms)
- Seamless integration with Phase 1 budget

---

### Task 5: Build Integration Tests

**Effort**: 1.5 hours

**Purpose**: Validate semantic search accuracy and performance.

**Script**: `scripts/test-semantic-search.py`

**Test Categories**:

1. **Semantic Accuracy Test**:
   - Known query → expected patterns
   - Calculate precision, recall, F1 score
   - Target: >85% accuracy

2. **Performance Test**:
   - Query response time
   - Embedding generation time
   - ChromaDB lookup time
   - Target: <200ms query time

3. **Hybrid Scoring Test**:
   - Verify semantic + metadata balance
   - Test edge cases (old but relevant, recent but irrelevant)
   - Validate final rankings

4. **Recommendation Quality Test**:
   - Diversity of recommendations
   - Relevance to task context
   - Avoidance of redundancy

5. **Integration Test with Phase 1**:
   - Semantic search → budget constraints
   - Verify token limits respected
   - Validate end-to-end pattern loading

**Test Cases**:
```python
# Test 1: Exact match query
query = "dbt error handling patterns"
expected = ["dbt-error-patterns.md", "dbt-best-practices.md"]
results = search(query, top_k=5)
assert expected[0] in [r.file for r in results[:3]]

# Test 2: Semantic similarity
query = "How to fix broken Snowflake queries?"
expected_contains = "snowflake" or "query" or "optimization"
results = search(query, top_k=5)
assert any(keyword in r.content.lower() for r in results for keyword in expected_contains)

# Test 3: Performance
start = time.time()
results = search("Tableau dashboard patterns", top_k=10)
duration = time.time() - start
assert duration < 0.200  # <200ms

# Test 4: Budget integration
recommendations = recommend("Create dbt models", top_n=20)
budget = MemoryBudget(max_tokens=20000)
loaded = budget.load_patterns_with_budget(recommendations)
assert budget.current_tokens <= 20000
```

**Success Criteria**:
- >85% semantic accuracy
- <200ms query time
- All integration tests passing
- Budget constraints respected

---

### Task 6: Update Documentation

**Effort**: 1 hour

**Files to Update**:
1. `projects/active/ai-memory-system-improvements/README.md`
2. `projects/active/ai-memory-system-improvements/context.md`
3. `projects/active/ai-memory-system-improvements/tasks/phase3-implementation.md`
4. Create `PHASE3-COMPLETION-REPORT.md`

**Content**:
- Phase 3 completion status
- Semantic search capabilities
- Usage instructions
- Performance metrics
- Integration with Phases 1 & 2

---

## Technical Specifications

### Vector Embedding Model

**Model**: `sentence-transformers/all-MiniLM-L6-v2`

**Why This Model**:
- Lightweight: 22.7M parameters (fast inference)
- Fast: ~500 sentences/second on CPU
- Accurate: 68.06 on STS benchmark
- Maintained: Active development by UKPLab
- Local: No API calls required

**Embedding Dimensions**: 768

**Similarity Metric**: Cosine similarity

### Vector Database

**Database**: ChromaDB

**Why ChromaDB**:
- Local-first: No cloud dependencies
- Fast: In-memory + persistent storage
- Simple API: Minimal learning curve
- Metadata filtering: Rich query capabilities
- Python-native: Easy integration

**Storage Location**: `.claude/vector-store/`

**Persistence**: SQLite backend (automatic)

### Hybrid Scoring Formula

```python
# Semantic similarity (from ChromaDB)
semantic_score = cosine_similarity(query_embedding, pattern_embedding)  # 0.0 - 1.0

# Metadata scores (from Phase 1)
recency_score = calculate_recency_score(last_used)      # 0.0 - 1.0
usage_score = calculate_usage_score(use_count)          # 0.0 - 1.0
confidence_score = confidence / 1.0                      # 0.0 - 1.0

# Weighted combination
final_score = (
    semantic_score * 0.60 +      # Primary: semantic relevance
    recency_score * 0.15 +       # Secondary: recent usage
    usage_score * 0.15 +         # Secondary: proven utility
    confidence_score * 0.10      # Tertiary: validation
)
```

**Rationale**:
- **60% semantic**: Primary signal - pattern content matches query intent
- **15% recency**: Favor recent patterns (reflect current state)
- **15% usage**: Proven patterns are more likely useful
- **10% confidence**: Validated patterns preferred

**Tuning**: Weights can be adjusted based on empirical results

---

## Performance Targets

| Operation | Target | Measurement |
|-----------|--------|-------------|
| **Embedding Generation** | <1s per pattern | Time to embed single pattern |
| **Query Response** | <200ms | Semantic search query time |
| **Recommendation** | <300ms | Pattern recommendation time |
| **Bulk Embedding** | <5min for 100 patterns | Initial embedding generation |
| **Semantic Accuracy** | >85% | Precision@5 on test queries |

---

## Dependencies

### Python Packages

```
# Add to projects/active/ai-memory-system-improvements/requirements.txt
tiktoken==0.5.1
sentence-transformers==2.2.2
chromadb==0.4.18
numpy==1.24.3
```

### System Requirements

- **Disk Space**: ~500MB for sentence-transformers model + ChromaDB
- **Memory**: ~1GB RAM for in-memory vector store
- **CPU**: Multi-core recommended for faster embedding generation

---

## Risk Assessment

### Identified Risks

1. **Model Download Size** (~80MB)
   - **Mitigation**: One-time download, cached locally
   - **Impact**: Low - acceptable for offline capability

2. **Embedding Generation Time** (~1s per pattern)
   - **Mitigation**: Incremental updates, background processing
   - **Impact**: Low - one-time cost per pattern

3. **Query Latency** (potential <200ms miss)
   - **Mitigation**: In-memory ChromaDB, query caching
   - **Impact**: Medium - monitor and optimize if needed

4. **Semantic Accuracy** (might not hit 85%)
   - **Mitigation**: Hybrid scoring adds metadata signals
   - **Impact**: Medium - fallback to keyword search if needed

### Mitigation Strategies

- **Performance Monitoring**: Log all query times, identify slow patterns
- **Incremental Rollout**: Test with small pattern subset first
- **Fallback Mechanism**: If semantic search fails, use Phase 1 relevance scoring
- **Tuning Parameters**: Adjust hybrid scoring weights based on results

---

## Success Validation

### Quantitative Metrics

- ✅ >85% semantic search accuracy (Precision@5)
- ✅ <200ms query response time (95th percentile)
- ✅ <1s embedding generation per pattern
- ✅ 100% integration test pass rate

### Qualitative Metrics

- ✅ User can ask "have we solved this before?" → get relevant patterns
- ✅ Related patterns automatically discovered
- ✅ No manual keyword matching required
- ✅ Natural language queries work intuitively

### Integration Metrics

- ✅ Seamlessly works with Phase 1 budget system
- ✅ Respects Phase 2 tier structure
- ✅ No increase in context token usage
- ✅ Zero additional cloud dependencies

---

## Timeline

**Total Estimated Time**: 2-3 days

| Task | Effort | Dependencies |
|------|--------|--------------|
| Task 1: Setup | 30 min | None |
| Task 2: Embeddings | 2 hours | Task 1 |
| Task 3: Semantic Search | 2 hours | Task 2 |
| Task 4: Recommendations | 1.5 hours | Task 3 |
| Task 5: Integration Tests | 1.5 hours | Task 4 |
| Task 6: Documentation | 1 hour | All tasks |

**Total**: ~8.5 hours (can be done in 2-3 focused sessions)

---

## Next Steps (Immediate)

1. ✅ Create this implementation plan
2. Set up vector embedding infrastructure
3. Build pattern embedding generator
4. Implement semantic similarity search
5. Create pattern recommendation engine
6. Build integration tests
7. Update documentation
8. Commit Phase 3 completion

---

## Related Work

**Research Foundation**: `tasks/research-findings.md` (A-MEM paper, Anthropic guidance)
**Phase 1**: Token-aware memory loading (foundation)
**Phase 2**: Memory consolidation pipeline (lifecycle management)
**Phase 3**: Semantic search (THIS PHASE - intelligent retrieval)

---

*This implementation plan provides step-by-step guidance for Phase 3 delivery in 2-3 days.*
