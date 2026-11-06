"""Record clarified method only;no SDK/source imports or experimental work."""
from pathlib import Path
import json,hashlib
from fractions import Fraction
D=Path(__file__).resolve().parent;ROOT=D.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((D/'persistence-verification.json').read_text())
for n,h in old['files_sha256'].items():assert sha(D/n)==h,n
reserve=(1050000*5+8192*15)*Fraction(11,10)
u=(55*64000+165*8192)//10
assert reserve==5910168 and u==487168
assert 3*reserve<=20000000<4*reserve and 12*u==5846016
# Check worst required reservation before each of twelve trusted settlements.
for k in range(12):assert k*u+reserve<=20000000
result={
 'phase':'P18_PARENT_CLARIFIED_ZERO_COUNT_METHOD_ADDENDUM',
 'status':'METHOD_FEASIBLE_FOR_MINIMAL_R02',
 'live_accepted':False,'EXECUTE_created':False,'producer_code_reviewed':False,
 'authority_source':'Current parent codex_delegation from01a1ada7-ffb8-73ad-bb44-6a1db859003c;corrects own technicalparameterinterpretation,not a fabricatednewusergrant',
 'clarification':'64000wasparenttechnicalparameter,notuserimmutablehardcap;localadmissionESTIMATE/actualusagequalificationhaltallowedwithoutnew64kconsent',
 'prior_64k_hard_guarantee_rejection_preserved':True,
 'prior_assertion_new_user_consent_required_superseded_by_current_parent_clarification':True,
 'no_wait_for_void_async_choice':True,
 'finance':{'reserve_microUSD':5910168,'trusted_valid_max_U_microUSD':487168,'twelve_trusted_valid_U_microUSD':5846016,'three_unknown_microUSD':17730504,'four_unknown_microUSD':23640672,'count_requests':0,'count_unit_price':'UNKNOWN_NOT_FREE','invoice':None,'currency_rounding':'ceil each Fraction upper to integer microUSD;no floats','invariant':'settled_upper+unknown_full_reserves+open_reserves+nextreserve<=20000000beforeeachdispatch','settlement_upper_formula_microUSD':'ceil((55*actual_input+165*actual_output)/10)','assumptions':['Pinned gpt-6.1-sol Standard/default implicit30m servicecontract honored','Outputmax8192 inclusive hidden/reasoning;modelcontext<=1050000;region10%included','Noadd-onbillables/12h/fast/hostedtools/autoSDKretry;allpossiblychargeddispatchesjournaled','Unknown/mismatch/timeoutretainR,halt;releaseonlycrediblevalidU,noinvoicerefundclaim']},
 'input_target':{'local_target':64000,'provider_enforced_64000_hard_limit_claimed':False,'actual_above_target':'retainrawresponse/cost/fullreserve;halt;notqualified;remainingNOT_RUN','new_version_registration_required':True},
 'unchanged_user_constraints':['inclusiveUSD20','one60minwallincludingcleanup','output8192','max12generationincludingretries/perroundretrycap','sameIPfrozenB/Cbenchmark1sessionx3roundeach','publicpromptallowlist/ownhistory/all6freeze-before-score/oldunknowns/G1reuse','noadditionalDUT/native/crossIP'],
 'current_next_step':'MinimalnewR02preparationonly;sealedsource/independentP18/exactEXECUTEstillneeded;R01countfeeblocknotclosed',
 'primary_sources_prior_read_not_refetched':['https://developers.openai.com/api/docs/models/gpt-6.1-sol','https://developers.openai.com/api/docs/guides/prompt-caching','https://developers.openai.com/api/docs/guides/token-counting','https://developers.openai.com/api/reference/ruby/resources/responses/methods/create'],
 'hallmark':{'considered':True,'read_this_round':False,'prior_read_reference':'hallmark-method-usage.json cites actual priorP18tools.skills__read for SKILL/review-finish,sameversionverifiedin persistence-verification.json','applied_for':['Preservehistoryandcurrentclarificationsource','Separatemethodfeasibilityfromsealedimplementationacceptance','Minimalsurgicalscopeandrankrealconstraints'],'workflow_executed':False,'scripts_executed':False,'not_applicable_reason':'UIworkflowdoesnotproveAPIpricing/resourcecontrol;technicalreasoningindependent'},
 'old_checkpoint_sha256':old['files_sha256'],
 'addendum_md_sha256':sha(D/'parent-clarification-method-addendum.md'),
 'command':'PYTHONDONTWRITEBYTECODE=1 python3 docs/audits/agent_bridge_2026-11-06/P18_bc_retest_preflight/record_parent_clarification.py',
 'exit_code':0,'API_key_reads_compile_sim_native_network_producer_tests':0,
 'write_scope':'P18reviewerownedonly;oldcheckpointsandproducer/shareddocs/indexunchanged'
}
with (D/'parent-clarification-method-addendum.json').open('x') as f:json.dump(result,f,indent=2)
print(json.dumps({'status':result['status'],'live_accepted':False,'reserve_microUSD':5910168,'old_checkpoints_unchanged':True,'addendum_json_sha256':sha(D/'parent-clarification-method-addendum.json')}))
