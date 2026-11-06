"""Versioned alarm attribution after independent Claude scope review. No oracle edits."""
from controller_done_score import adjudicate as previous,position


def adjudicate(label,result):
    row=previous(label,result)
    alarms=sorted({tuple(x) for p in result['properties'] for x in p['failures']},key=position)
    end=(label.get('cycles',0)-1,'post');ordinary=[p for p in alarms if p!=end]
    first=label.get('first_safety_failure');early=[]
    if first:
        onset=(first['cycle'],first['phase']);early=[p for p in alarms if position(p)<position(onset)]
        row['definite_detection']['safety']=result['complete'] and not early and any(position(p)>=position(onset) for p in ordinary)
    else:row['definite_detection']['safety']=False
    early_end=[p for p in alarms if position(p)<position(end)]
    row['definite_detection']['input_completion']=bool(row['eligible']['input_completion'] and result['complete'] and end in alarms and not early_end)
    row['fully_resolved_detection']={k:bool(v and row['fully_resolved_context']) for k,v in row['definite_detection'].items()}
    row.update(ordinary_alarm_samples=len(ordinary),marker_alarm=bool(end in alarms),early_finite_alarm_samples=len(early_end),
        marker_safety_signal=bool(first and result['complete'] and end in alarms and not early),
        marker_only_safety_signal=bool(first and result['complete'] and end in alarms and not ordinary),
        category_attribution='UNATTRIBUTED_ANY_SLOT; strata describe eligible DUT cases, not proven monitor obligation/category',
        safety_credit_excludes_marker=True,finite_credit_requires_no_earlier_alarm=True)
    return row
