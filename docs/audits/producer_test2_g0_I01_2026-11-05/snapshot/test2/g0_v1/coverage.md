# D01 44 项映射 — I01

仅对应新 G0 合成元数据测试。METADATA_TESTED 不表示真实 DUT/native/monitor 科学验证；PARTIAL_METADATA_ONLY 只验证声明／字节／身份，未提供原始科学解析。所有科学归因均 NOT_EVALUATED。精确 fixture/result SHA 见新结果 coverage-map.json。

P08 仅接受封存 D01 纸面设计（PASS_WITH_LIMITS），不接受 I01 代码。P08-N1 的现有代码追踪：`adapter.py:162` 的 `terminal()` 将缺 terminal 设为持久 `gap=True`；`take():160` 和主循环 `:180` 拒绝后续 dispatch/request flags。匹配 error 则消费 terminal 并保留未知成本，不设置缺 terminal 的 gap。已有 test_06 / test_83 保存缺 terminal 的 UNRESOLVED，test_07 / test_08 保存匹配 error 的 UNRESOLVED，test_16 拒绝交错；这些不是“缺 terminal 后再次派发”或“匹配 error 后合法 retry”的专门组合测试。test_69 的合法 retry 是 input-cap 路径，不能冒充 error-retry 测试。上述两条专门路径未新测，留给 P09 判断覆盖缺口；本次仅只读代码追踪，不扩充测试或改 D01。

| D01 | 支持状态 | 新测试 | 实际范围／未实现部分 |
|---|---|---|---|
| FM01 | METADATA_TESTED | test_05_missing_returned_claims_success | Successfulclaimedreturnedmissing rejected |
| FM02 | METADATA_TESTED | test_06_missing_generation_terminal_unknown, test_07_generation_transport_error_unknown, test_08_count_transport_error_unknown, test_83_missing_count_terminal_unknown | Credibleerrors/missingterminals UNRESOLVED;usage null |
| FM03 | METADATA_TESTED | test_03_duplicate_event, test_68_duplicate_response_correlated, test_71_duplicate_call, test_84_duplicate_request_correlated | Event/call/request/response duplicate identities rejected |
| FM04 | METADATA_TESTED | test_04_orphan_terminal | Terminal request identity must match dispatch |
| FM05 | METADATA_TESTED | test_72_orphan_dispatch, test_82_missing_call_inventory | Orphan dispatch/missingcall inventory rejected |
| FM06 | METADATA_TESTED | test_16_illegal_order | Strictserializedorder rejectsinterleaving |
| FM07 | METADATA_TESTED | test_39_concurrency_unsupported | Concurrentformat unsupported andfailsclosed |
| FM08 | METADATA_TESTED | test_11_session_mismatch | CorrelatedcontextSHArebinding stillrejects wrongsession identity |
| FM09 | METADATA_TESTED | test_10_context_mismatch, test_70_retry_cap_reached | Contextidentity/retryindexandcap binding |
| FM10 | METADATA_TESTED | test_12_prompt_mismatch, test_13_schema_digest_mismatch | Promptbytes/messages/schemaSHA binding;notopaquecontentsecrecyproof |
| FM11 | METADATA_TESTED | test_14_response_mismatch | Responsebody identity andacceptedsnapshot binding |
| FM12 | METADATA_TESTED | test_17_halt_retry | Posthalt same-roundretry REJECT |
| FM13 | METADATA_TESTED | test_18_halt_round | Posthalt crossround REJECT |
| FM14 | METADATA_TESTED | test_19_halt_session | Posthalt crosssession REJECT |
| FM15 | METADATA_TESTED | test_20_halt_flags | Posthalt requestflags REJECT |
| FM16 | METADATA_TESTED | test_21_halt_orphan_dispatch, test_72_orphan_dispatch | Posthalt/orphan dispatch REJECT |
| FM17 | METADATA_TESTED | test_22_legal_halt_notrun | LegalNOT_RUN preserved withnullactualtokens |
| FM18 | METADATA_TESTED | test_79_late_terminal_after_halt_retains_known_usage, test_80_late_error_after_halt_unknown_usage, test_81_late_terminal_not_accepted_candidate | Pendinghaltlate terminal retainsknowncost orUNKNOWN;noresumingorcandidateacceptance;integrityUNRESOLVED |
| FM19 | METADATA_TESTED | test_06_missing_generation_terminal_unknown, test_64_missing_usage_subsets_null, test_90_missing_usage_cannot_be_zero_filled | Missingusage/subsetsnull;zero-filledfailure rejected |
| FM20 | METADATA_TESTED | test_23_usage_arithmetic_correlated, test_24_usage_subset_correlated, test_31_raw_usage_mismatch | Correlatedarithmetic/subset/rawusageerrors rejected |
| FM21 | METADATA_TESTED | test_25_model_mismatch, test_26_tier_mismatch, test_61_correlated_returned_model, test_62_correlated_returned_tier | Requestedandcorrelatedreturnedmodel/tier mismatches rejected |
| FM22 | METADATA_TESTED | test_15_parent_count_mismatch, test_27_count_mismatch | Parentcount IDandactualinputcount binding |
| FM23 | METADATA_TESTED | test_28_count_quota, test_63_generation_quota, test_70_retry_cap_reached, test_86_generation_reserve_cap, test_88_total_reserve_cap | Count/generation/retry/reserve cap violation rejected |
| FM24 | METADATA_TESTED | test_13_schema_digest_mismatch, test_33_manifest_sha_tamper, test_34_release_digest, test_89_missing_source_binding | Rawbyte/source/schema/manifest/releaseSHA binding |
| FM25 | METADATA_TESTED | test_54_relative_path_escape, test_55_symlink_input, test_56_output_refuses_overwrite, test_57_output_symlink, test_77_output_path_escape, test_87_output_parent_symlink | Traversal/symlink/overwrite boundary negativecontrols |
| FM26 | OUT_OF_SCOPE_RAW_PARSER | test_75_unsupported_raw_parser_claim, test_46_unanchored_metadata_upgrade | OnlymetadataSHA/identity;two summariescannotestablishrawindependentchain |
| FM27 | PARTIAL_METADATA_ONLY | test_59_missing_artifact, test_33_manifest_sha_tamper | Genericfilepresence/hashonly;noVCDheader/step/inputparser |
| FM28 | OUT_OF_SCOPE_RAW_PARSER | test_33_manifest_sha_tamper | NoVCD-to-literaltransportparserorphysicalinputcomparison |
| FM29 | OUT_OF_SCOPE_RAW_PARSER | test_75_unsupported_raw_parser_claim | No dualphysicalPRE/POSTsemanticcomparison |
| FM30 | PARTIAL_METADATA_ONLY | test_42_phase_mismatch, test_43_prefix_mismatch, test_60_wrong_phase_type | Declaredcycle/phase/resettypesandboundariesonly;no rawlogparser |
| FM31 | PARTIAL_METADATA_ONLY | test_33_manifest_sha_tamper, test_45_checker_sha_mismatch | Artifact/sourcehashreferencesonly;no HEX/rows decoder |
| FM32 | OUT_OF_SCOPE_RAW_PARSER | test_46_unanchored_metadata_upgrade, test_75_unsupported_raw_parser_claim | No MON/propertyrawparser;scientificupgrade rejected |
| FM33 | PARTIAL_METADATA_ONLY | test_40_reduced_metadata_vector_scope_only, test_41_slot_missing, test_60_wrong_phase_type | Declaredwidth/slot/phasetypesbound;no rawVCD/bit observations |
| FM34 | PARTIAL_METADATA_ONLY | test_44_unknown_bit_not_alarm | Declaredunknownflag allowed;scienceNOT_EVALUATED,notphysicalalarm |
| FM35 | PARTIAL_METADATA_ONLY | test_42_phase_mismatch, test_43_prefix_mismatch | Declaredprefix/pre-postboundary checked;no oracle/categorytruth |
| FM36 | PARTIAL_METADATA_ONLY | test_48_fake_reference_verdict | No oracleinvocation;non-nullreferenceverdict isrejected |
| FM37 | PARTIAL_METADATA_ONLY | test_45_checker_sha_mismatch, test_89_missing_source_binding | Syntheticdescriptor/sourceSHAonly;no realcheckerloadingorcorrectness |
| FM38 | PARTIAL_METADATA_ONLY | test_38_no_historical_identity_fabrication, test_91_no_independent_anchor_upgrade | Historicalidentityfabrication/independentanchorupgrade rejected;actualanchorauthenticitynotverified |
| FM39 | PARTIAL_METADATA_ONLY | test_46_unanchored_metadata_upgrade | Newmetadata schemarejectsconfirmed=true;oldP05-N1helper/backlog unchanged |
| FM40 | OUT_OF_SCOPE_G1 | test_75_unsupported_raw_parser_claim | NoX-to-anyseq/4statesemanticproof;scientificclaimsnotavailable |
| FM41 | OUT_OF_SCOPE_G1 | test_47_completion_upgrade, test_75_unsupported_raw_parser_claim | Noformal/vacuity/128completionproof;upgrades rejected |
| FM42 | PARTIAL_METADATA_ONLY | test_49_prompt_visibility_leak, test_73_hidden_candidate_input_correlated, test_92_release_before_freeze | Explicitartifactvisibility/allowlistandreleaseflags;no semanticprivacyoractualrendererproof |
| FM43 | PARTIAL_METADATA_ONLY | test_52_notreached_retained, test_53_invalid_retained, test_82_missing_call_inventory | Attemptinventory/INVALID/NOT_REACHED/unknown retained;no realfault/RTLcoverage denominators |
| FM44 | METADATA_TESTED | test_36_template_not_release, test_37_template_not_grant, test_93_offline_grant_not_execution_grant | Templates/executiongrant claims refused;offlineauthorizationdescriptionneverexecutes |
