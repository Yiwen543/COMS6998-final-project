<verification_plan>

1. **Semantic evidence.** CVDP supplies no E-graph. The reviewed adapter extracts
   this pinned arbiter's guards and actual egg saturation joins the compact and
   De Morgan-expanded form of each winning predicate. There are 16 distinct
   winning roots (eight request, eight override), not one equivalence class of
   all winners. Request k requires reset=0, override=0, req[k]=1 and all lower
   request bits zero. Override k requires reset=0, a nonzero override, bit k set
   and lower override bits zero. These are pure binary predicates. Clock/reset
   event context stays outside equality rewriting.
2. **Corner cases.** Idle, every winning index, multiple requests with different
   priorities, override without matching requests, conflicting request/override,
   multi-bit override, reset while a grant is active, and recovery. The final
   override fallback is unreachable under its enclosing nonzero guard.
3. **Stimulus.** Drive on falling edges, check hold behavior after 1 ns, then
   sample 1 ns after rising edges. Use a four-cycle starter, a second run with
   18 additional directed vectors derived from uncovered predicates/spec probes,
   and a separate exhaustive binary-pair reference. The default standalone
   testbench executes all 65,536 request/override pairs plus reset probes in one
   simulation. This is input exhaustion, not exhaustive temporal verification.
4. **Checkers.** Independently compute selected = override != 0 ? override : req,
   isolate its lowest set bit arithmetically, compare grant/valid and valid/reset
   index, and verify output stability between rising edges. Reset clears all
   outputs at the next rising edge. Count failures and terminate nonzero in
   standalone mode. Stimulus partition masks are diagnostic functional tracking,
   separate from measured DUT coverage. Keep the benchmark RTL unchanged.

</verification_plan>
