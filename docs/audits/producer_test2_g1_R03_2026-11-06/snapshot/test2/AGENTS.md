# test2: separately registered property-generation experiment

This user-authorized task evaluates generated monitors, not generated stimulus.
The old stimulus-difficulty/B-before-C selection gate does not define this task.
Do not tune this new study against C results or overwrite any historical result.

Claude exclusively authors the independent specification checker. GPT authors
infrastructure and experimental candidate monitors. These are separate artifacts.
No GPT-authored FIFO oracle may be silently substituted for the Claude oracle.

Candidate model packets are explicit allowlists. Never expose private/, reference/,
mutant sources, held-out actions/observations, reference source, expected answers,
upstream FORMAL assertions, maintainer instructions, or evaluation outcomes.
Candidate code is passive and is not a scoring oracle. Freeze candidate hashes
before final scoring. Keep every failed/unknown/unobservable result.

Registration v1 commits the methodology and numeric caps before model calls.
Final live freeze is a separate artifact, requiring independent reference review,
control validation, fault observability, semantic/source checks and runner audit.
Changing anything material before that freeze needs an explicit version/history.
