# trace_done paid preflight v1 — gates not passed

2026-11-05. Current Git main HEAD c25180848ebfe9a1f49da0aa5f579cac913e6428. User authorized USD9:one independent Claude review(maxUSD4) andfourOpenAIinputcounts(reserveUSD5),no generation/author. No experiment result is changed to PASS.

## Actual requests and failure

One claude-opus-5-5 fresh/tool-free CLI invocation failed with ENOTFOUND after internal transport retries. CLI reports is_error=true,USD0,input0/output0,no review artifact/verdict. It is UNKNOWN/FAILED,not acceptance. The first invocation incorrectly used restricted default network: credential-free control confirms DNSfailure there, while elevated network using existing httpx with TLS validation reachesAnthropicHTTP404. A default urllib trust-store error is separately retained; verification was not disabled. Failure was an execution-mode mistake. No second role invocation has run; providerHTTPrequestcount is not observed directly.

Four actual gpt-6.1-sol input-count requests succeeded,0generation:

|Arm|Initial|Unchanged history stress|64k history gate|
|---|---:|---:|---|
|B|44022|66538|FAIL|
|C|47651|70167|FAIL|

Counts include strictschema/format/role overhead via the exact structured API payload. These are measured payload lengths,not generated/billed-model-token usage. Count-endpoint fees are not reported; total spend is unknown beyond CLIreportedUSD0. No free-cost or tokenROI claim. PromptSHAs match approved proposal. No candidate generated,oracle revised or retry issued.

## Offline recovery prepared

New `controller_done_prompt_v2.json` registers common lossless column compression before any additional paid request. Original public packets,failedcounts and scope-v2 reviewpacket stay intact. All3168counteridentities/all230devcycles/DUT/RTL/spec/oracle/seeds/semanticgroups/guards/targets/budgets preserved. Restoring new packet gives canonicalJSON equal to v1,including JSONtypes. B/C common identical. Compact common packet bytes112817→101425;C125452→114060. These are bytes,not measured tokens,and do not establish passing64k.

The16000byte candidate/6×400description/18000characterhistory stress is unchanged; no easierprobe or largerbudget. New36roundmock+36roundreplay completed with exactmatching prompts/sources/developmentfeedback. Everycandidate source matches oldarm-blindmock; oldindependentgrading reused explicitly,not rerun/not newLLMeffectevidence. Five codec/type/fullpacket/isolation/replay tests pass in controller-done-codec-v2-tests.log. No newDUTsimulation/formaljob. Source snapshots and generation-source hash retained,including generic JSONtype equality hardening that leaves actual packet bytes unchanged.

Original3486/212/239parentmembers,two oldscores and all76-test offlineacceptance evidence files verified unchanged afterstage. Fournewpreflight tests passed earlier in this stage,not another full80test invocation. Both staged keys remain0600 and retained while preflightqualification is unresolved; values never printed,and no repeatedkeyrequest.

## Next bounded authorization

Ready `axis_length_done_v1/qualification/api-preflight-v3/proposal.json`:request one additional Claude review of exactly the same scope-v2 packet,under elevated network;plusfournewcounts of compressedsharedpacket,with same model/stress/64kcap and0generation. FirstClaude attempt reportedUSD0; proposed combined ceiling remains originalUSD9(Claude<=4,countfeeswithinUSD5reserve,feeunconfirmed),nowexplicitly2CLIinvocationsincludingfailure/8counts includingoriginalfour. No authorizationv2 exists and no newrequest has run. Current B/C live remains closed. Existing keys can serve the approved recovery stage without restaging.
