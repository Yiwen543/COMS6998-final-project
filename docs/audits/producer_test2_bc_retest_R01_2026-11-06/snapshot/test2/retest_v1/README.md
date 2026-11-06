# Known-benchmark B/C retest adapter v1 — offline preparation

User approved a new same-IP old-benchmark retest: B raw/common versus C same plus
verified Egraph,one session each,three rounds,USD20 inclusive API ceiling. Schedule
is B1,C1,C2,B2,B3,C3. This is not a new hidden set or isolated semantic-causation
study. Old source/reference/data/freezes/results remain unchanged.

**Live remains blocked:** count endpoint fee is UNKNOWN. No count/generation,
SDK construction or credential read is allowed before inclusive verified billing,
exact independent precheck and coordinator EXECUTE. A later zero-count alternative
requires a separately reviewed version;this code does not silently assume free
counts or use a local token estimate as an exact64k admission check.

## Boundaries

- Max12generation+16count reservations including4preflight counts,one manual
  failure retry/round,SDK retry0. Modelgpt-6.1-sol/low,Standard/default,64kinput/
  8192output/120s;storefalse,implicit30mcache. Generation reserve241920microUSD
  each;count reserve must be known and full worstcase<=20,000,000microUSD.
  Failed/timeout/unknown reservations are never refunded or treated as free.
  Actual invoice remains UNKNOWN;reported cache/reasoning subsets not added twice.
- Max12monitor compile roots(Yosys/Icarus,60s),990monitor replay roots(vvp,15s),
  204444cycles. NewDUT/native/setup/versionquery0. Grading uses old qualified
  observations and sharedv4case engine. All6snapshots—includinginvalid/NOT_RUN—
  freeze before hidden scoring. Twofinals use lastcompilevalid. Oldraw12/N10/
  38oracleunknowns and all failures remain;no oldformal540/74witness rerun.
- Parent starts one3600s monotonic window before live gate checks,supervises one
  owned stage PGID. Worker/API/local descendants stay in that group. Work stops
  at3590s,parent forces cleanup at3595s,final deadline3600s. Per-child timeout is
  min(singlecap,remainingwork). Reservations persist before dispatch and time is
  rechecked afterward. Fatal Halt deliberately escapes old per-case Exception
  handling. Interrupted grading retains972planned cases as unresolved/recorded.
  Parent cleanup covers registered nondetached children,not hostile descendants,
  OS/filesystem hard realtime or whole-host resources;observed overruns fail.
- Worker lease binds supervisor/start/output/group. SDK helper requires exact
  live ledger,open reservation,payload/schema/price binding and parent/group;
  eachreservation has an exclusive claim. Direct helper execution cannot reuse
  one attempt to bypass quotas. API-only process reads staged key after gates;
  no key appears in logs/prompts/manifests. Parent/localenv has no credentials.
- Only original public packets/header/system plus own lastcandidate/devfeedback
  reach the provider. Maintainer source/reference/private/final/skills stay out.
  No tools are given to the model. Claude oracle and all SV/driver/ABI unchanged.

## Implementation / usage

`resources.py`: inclusive persistent reservations/window;`release.py`:six-round
release;`supervision.py`:bounded parent/child lifecycle;`api.py`:isolated SDK action;
`gates.py`:new exact review/pricing/source gate;`pipeline.py`:minimal orchestration
using frozen compiler/runtime/grader;`cli.py`:only supervised stage entry.

The authorized live root is fixed to test2/results/controller-done-bc-retest-v1,
created exclusively once. The parent has a separate -supervision directory.
`--worker` is internal and requires the parent lease. No EXECUTE is supplied here.

`python test2/retest_v1/cli.py --mode live --output <registered-root> --execute <exact-receipt>`

Offline mock uses fakeAPI/fakeSVtools;offline replay accepts mock sources only,
so it cannot silently add another real-tool pass after a live cohort. No mode
restarts an existing run. Preserve raw logs/ledger after every failure.

## Saved verification,with exact scopes

- Preliminary fullmock:6snapshots/2finals,12fakecompile/990fakereplay/204444cycles,
  all6rounds38oracleunknown;actualAPI/SV0.
- Initial18-case integration:1failure retained. Relative output paths caused
  scoring provider ValueError and162unresolved/candidate. Fixed by normalizing
  output paths,not relaxing score expectations.
- Revised19-case integration:19PASS,including fullmock/replay with original
  38unknowns and identical endpoints,allfailed retrycaps,usage preservation,
  cancellation972case matrix,priceunknown/USD20 limits and fake deadlines.
- Final SDK lease/reservation deltas:6targeted purechecksPASS. Fullmock/replay
  source version precedes these guard/resource-release additions;it was not
  rerun after the parent's explicit stop-repeating instruction. Finaldelta
  copies/hashes are saved for independent review. Do not describe all25 as one
  final-source fullsuite,or fake data as actual LLM/SV qualification.

Actual SDK/API/key-content reads/process/signal/SV calls0 throughout preparation.
Credential metadata alone was checked after user staged it:present/nonempty/
regular0600,parent0700. Key retained for the authorized stage,not reopened here.
