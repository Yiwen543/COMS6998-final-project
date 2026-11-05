KEYS=['i_reset','i_mcyc','i_mstb','i_mwe','i_maddr','i_mdata','i_msel','i_sstall','i_sack','i_sdata','i_serr','o_mstall','o_mack','o_mdata','o_merr','o_scyc','o_sstb','o_swe','o_saddr','o_sdata','o_ssel']

def _row(c,**kw):
    pre={k:0 for k in KEYS}
    pre.update(kw)
    post={k:0 for k in KEYS if k.startswith('o_')}
    return {'cycle':c,'pre':pre,'post':post}

def _base():
    return [_row(0,i_reset=1),_row(1,i_reset=1)]

def _wr(sd=0xAB,sa=0x05,ss=0,sel=0xF):
    rows=_base()
    rows.append(_row(2,i_mcyc=1,i_mstb=1,i_mwe=1,i_maddr=0x05,i_mdata=0xAB,i_msel=sel))
    rows.append(_row(3,i_mcyc=1,o_scyc=1<<ss,o_sstb=1<<ss,o_swe=1<<ss,o_saddr=sa<<(8*ss),o_sdata=sd<<(32*ss),o_ssel=sel<<(4*ss)))
    rows.append(_row(4,i_mcyc=1,o_scyc=1<<ss,i_sack=1<<ss))
    rows.append(_row(5,i_mcyc=1,o_mack=1))
    rows.append(_row(6))
    return rows

def _rd(md=0x55):
    rows=_base()
    rows.append(_row(2,i_mcyc=2,i_mstb=2,i_maddr=0x12<<8,i_msel=0xF<<4))
    rows.append(_row(3,i_mcyc=2,o_scyc=2,o_sstb=2,o_saddr=0x12<<8,o_ssel=0xF<<4))
    rows.append(_row(4,i_mcyc=2,o_scyc=2,i_sack=2,i_sdata=0x55<<32))
    rows.append(_row(5,i_mcyc=2,o_mack=2,o_mdata=md<<32))
    rows.append(_row(6))
    return rows

def _unm(ack=False):
    rows=_base()
    rows.append(_row(2,i_mcyc=1,i_mstb=1,i_maddr=0x40,i_msel=0xF))
    rows.append(_row(3,i_mcyc=1))
    if ack:
        rows.append(_row(4,i_mcyc=1,o_mack=1))
    else:
        rows.append(_row(4,i_mcyc=1,o_merr=1))
    rows.append(_row(5))
    return rows

def _shift(rows,off):
    return [{'cycle':r['cycle']+off,'pre':r['pre'],'post':r['post']} for r in rows]

def _early_err():
    rows=_base()
    rows.append(_row(2,i_mcyc=1,i_mstb=1,i_maddr=0x05,i_msel=0xF))
    rows.append(_row(3,i_mcyc=1,o_merr=1))
    rows.append(_row(4))
    return rows

def _early_err_then_reset():
    return _early_err()+[_row(5,i_reset=1)]+_shift(_wr()[2:],4)

def _slave_err():
    rows=_base()
    rows.append(_row(2,i_mcyc=1,i_mstb=1,i_maddr=0x05,i_msel=0xF))
    rows.append(_row(3,i_mcyc=1,o_scyc=1,o_sstb=1,o_saddr=0x05,o_ssel=0xF))
    rows.append(_row(4,i_mcyc=1,o_scyc=1,i_serr=1))
    rows.append(_row(5,i_mcyc=1,o_merr=1))
    rows.append(_row(6))
    return rows

def _abort_fwd(fwd,bad=None):
    rows=_base()
    rows.append(_row(2,i_mcyc=1,i_mstb=1,i_mwe=1,i_maddr=0x05,i_mdata=0x10,i_msel=0xF))
    rows.append(_row(3,i_mcyc=1,i_mstb=1,i_mwe=1,i_maddr=0x06,i_mdata=0x11,i_msel=0xF))
    rows.append(_row(4))
    c=5
    for a in fwd:
        d=0x10+(a-5)
        if bad is not None and a==bad:
            d^=0x01
        rows.append(_row(c,o_scyc=1,o_sstb=1,o_swe=1,o_saddr=a,o_sdata=d,o_ssel=0xF))
        rows.append(_row(c+1,o_scyc=1,i_sack=1))
        c+=2
    rows.append(_row(c))
    return rows

def run(check_rows):
    tests=[
        ('write_positive',_wr(),'scoped_pass'),
        ('write_payload_fault',_wr(sd=0xAC),'dut_violation'),
        ('write_misroute_fault',_wr(ss=1),'dut_violation'),
        ('read_positive',_rd(),'scoped_pass'),
        ('read_data_fault',_rd(md=0x56),'dut_violation'),
        ('unmapped_err_positive',_unm(),'scoped_pass'),
        ('unmapped_ack_fault',_unm(ack=True),'dut_violation'),
        ('invented_ack_fault',_base()+[_row(2,i_mcyc=1,o_mack=1),_row(3)],'dut_violation'),
        ('incomplete_unresolved',_wr()[:4],'unresolved'),
        ('early_unexplained_err_unresolved',_early_err(),'unresolved'),
        ('unexplained_err_persists_after_reset',_early_err_then_reset(),'unresolved'),
        ('slave_err_positive',_slave_err(),'scoped_pass'),
        ('masked_lane_write_positive',_wr(sd=0x5500AB,sel=0x1),'scoped_pass'),
        ('enabled_lane_write_fault',_wr(sd=0xAC,sel=0x1),'dut_violation'),
        ('abort_nonoldest_forward_unresolved',_abort_fwd([6]),'unresolved'),
        ('abort_both_forward_unresolved',_abort_fwd([5,6]),'unresolved'),
        ('abort_reverse_forward_unresolved',_abort_fwd([6,5]),'unresolved'),
        ('abort_none_forwarded_pass',_abort_fwd([]),'scoped_pass'),
        ('abort_enabled_byte_corrupt_fault',_abort_fwd([6],bad=6),'dut_violation'),
        ('abort_double_consumption_fault',_abort_fwd([6,6]),'dut_violation'),
        ('abort_then_reset_forward_fault',_abort_fwd([])[:5]+[_row(5,i_reset=1),_row(6,o_scyc=1,o_sstb=1,o_swe=1,o_saddr=6,o_sdata=0x11,o_ssel=0xF),_row(7,o_scyc=1,i_sack=1),_row(8)],'dut_violation'),
        ('unsolicited_slave_ack_env',_base()+[_row(2,o_scyc=1,i_sack=1),_row(3)],'input_or_scope_invalid'),
    ]
    out=[]
    for n,r,exp in tests:
        try:
            ok=check_rows(r)['verdict']==exp
        except Exception:
            ok=False
        out.append({'name':n,'pass':ok})
    return out




