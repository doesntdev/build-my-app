# AI feasibility: conditional specialist review

Read this only when the application includes an AI/LLM feature. First follow the
same general feasibility review as any other feature in [ideation](ideation.md).
AI is one specialist branch, not the default subject of the whole interview.
If live pricing or capability evidence is unavailable, mark it unverified and
keep the affected design provisional; do not invent a quote or block unrelated
no-cost discovery. Use the general risk/decision record rather than a parallel
AI-only acceptance process.

## Specialist questions and evidence

### LLM / AI exploration

Mentioning AI triggers exploration, not rejection or automatic Workers AI setup.
Ask in dependency order and reuse what the user already said:

1. **Job and quality:** What exactly will the LLM do: classify, retrieve, chat,
   take actions or generate long content? What is acceptable correctness and
   human review? Could rules, search, templates or a smaller model do it better?
2. **Work per outcome:** Input/output size, language, source material, tool calls,
   steps, revisions, retries and partial failures. Count every call, not just the
   final output. What may be sent to a provider, retained or reused for training?
3. **Demand:** Expected active users, uses per user/day/month and peak concurrency.
   Are anonymous use, shared links or free trials possible? Who can spend money?
4. **Experience and economics:** Interactive vs background; wait tolerance and
   delivery method; price/subsidy per completed outcome; monthly ceiling and
   limits when demand exceeds it. BYOK shifts billing, not privacy, UX or abuse
   obligations. Running a local model is not free hosting or free operations.

Compare a small set of plausible approaches against the quality target, not
merely advertised price: deterministic/no-model, an appropriate Workers AI model,
or an external model API when quality/privacy/capability warrants it. Do not
require an extra inference subscription merely to run this skill.

Fetch current official **model/API** prices, rate limits, context window,
maximum output, runtime limits and applicable long-context/region tiers. Save
model/version, currency/unit, source URL and date checked beside the estimate.
A consumer chat subscription is not evidence of production API entitlement or
unlimited app use. Context capacity is not maximum output capacity, and streaming
does not remove output, rate or execution limits. Don't claim either success or
impossibility for a long task without checking the selected model and job design.

### Make the unit economics visible

Calculate with a tool. Define the unit of value first (one completed book, report,
conversation, image), then aggregate demand. For token-priced inference:

```text
model_cost_per_job = sum_over_all_calls(
    input_tokens / 1,000,000 * applicable_input_rate
  + output_tokens / 1,000,000 * applicable_output_rate
  + other_billable_token_costs + tool_fees
)
monthly_jobs = active_users * jobs_per_user_per_month
monthly_cost = fixed_plan_costs + monthly_jobs * expected_cost_per_completed_job
             + other_usage_costs
```

Use provider-specific units for neurons, audio minutes, images or hosted tools;
never apply token prices to another unit. Include repeated context, planning,
critique/revision, failed/abandoned attempts and bounded retry overhead. Account
for billable reasoning tokens where applicable without double-counting the
provider's output total. Use cache/batch discounts only when the proposed flow
actually qualifies. Retried calls may bill even when the user never gets a result.

Show a compact comparison with:

- Per completed action, per active user and per month at expected usage.
- A growth case and a burst/abuse case, not only a single average user count.
- Fixed hosting/plan costs plus DB rows scanned/written, storage/retention,
  request/operation fees, egress where applicable, queues, email, observability,
  third-party tools and payment fees when relevant. Avoid double-counting free
  allocations or shared plan fees; never assume every service shares one quota.
- Assumptions, exclusions and uncertainty. A token-cost lower bound is not a full
  product quote or a measured latency/quality result. A 10x scenario and a retry
  reserve are not worst-case guarantees. Without caps, exposure can be unbounded.

### Worked scenario: a 100,000-word book

If the user says "the LLM writes a 100,000-word book," surface the implications
immediately. First clarify books per active user, desired quality, source length,
revisions and wait tolerance. Explain that long-form consistency, fact checking,
chapter planning and editing matter as well as the final token count.

The following is **illustrative arithmetic**, not an executed generation,
capacity test, quality endorsement or current quote. Recheck before reuse.
Assume English planning at 1.5 tokens/word (150,000 final tokens; actual tokenizer
and language differ), two full-text passes totaling 300,000 output tokens,
1,000,000 total input tokens across repeated chapter/context calls, and a 20%
retry reserve. Extra planning/review output and tool calls can increase this.
For 100 active users requesting two books each, demand is 200 books/month.

Documentation checked 2026-11-09; rates are USD per million uncached input/output
tokens, standard online processing, before free allowances/discounts/taxes:

| Example candidate | Input / output rate | Raw model cost/book | With retry reserve/book | Per active user (2 books) | 200 books/month | 10x demand (2,000 books) |
| --- | --- | --- | --- | --- | --- | --- |
| Workers AI `@cf/meta/llama-3.3-70b-instruct-fp8-fast` | $0.293 / $2.253 | $0.9689 | $1.16268 | $2.32536 | $232.54 | $2,325.36 |
| OpenAI `gpt-6.1-sol`, short-context price tier | $2 / $10 | $5 | $6 | $12 | $1,200 | $12,000 |

Sources: [Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/)
and [OpenAI API pricing](https://developers.openai.com/api/docs/pricing).
The total input is across multiple calls, **not** a claim that every call fits a
short-context tier; price each real call against its actual tier. These candidates
have not been qualified here for book quality, throughput or output length. The
cheaper model may fail the quality target; the dearer one is not automatically
better. A complete quote adds orchestration, hosting, storage, review and other
costs. Show honest ranges when actual call design or token volume is unknown.

Recommend testing an outline and one representative chapter first, then an
asynchronous, checkpointed chapter workflow with continuity summaries, editing,
export to private R2 and authenticated progress/delivery if the test succeeds.
Check per-step and whole-job time/token/rate limits. Bound concurrent jobs,
retries, revisions and maximum spend; preserve resumability and cancellation.
Streaming one HTTP response is not a durable book-production system. Offer the
full book path with realistic limits, a smaller initial outcome, or a different
quality/model approach. Let the user choose after hearing the estimate; do not
quietly replace "book" with "outline" or claim that one generation proves quality.

### Set guardrails before a metered prototype

Define server-side per-user/job quotas, input/output limits, bounded concurrency,
retry ceilings, idempotency and a global spend/admission budget. Reserve budget
atomically before starting work so concurrent requests cannot all pass the same
check; reconcile actual usage, handle uncertain provider charges and keep headroom
for in-flight work. Stop new admissions at the agreed limit, support cancellation
where the provider allows it, and explain charges that cancellation cannot undo.
A dashboard alert is not a hard cutoff, and an app estimate is not a provider
billing guarantee. Confirm exact data destination and budget authorization before
real inference; use deterministic fixture responses in ordinary local tests.


Carry product findings, estimates and evidence into the application's root
`spec.md`, linked to the affected requirement IDs. Keep execution authority in
the charter and derive experiments/implementation into the selected tracker.
Return to [ideation](ideation.md) to agree the affected feature's next step;
resolving AI costs does not establish feasibility of the rest of the application.
