class G:
    def __init__(self):
        self.rows = []
        self.st = {'scl': 1, 'sda': 1, 'scl_pin': 1, 'sda_pin': 1, 'valid': 0, 'ready': 0, 'rx_valid': 0, 'rx_data': 0}
        self.reset()
        self.reset()

    def row(self, act=None, **ov):
        a = {'rst_n': 1, 'target_ack': 1, 'enable': 1}
        a.update(act or {})
        s = dict(self.st)
        s.update(ov)
        self.rows.append({'cycle': len(self.rows), 'action': a, 'pre': s, 'post': dict(s)})

    def set(self, scl, sda):
        self.st.update(scl=scl, sda=sda, scl_pin=scl, sda_pin=sda)
        self.row()

    def start(self):
        self.set(1, 1)
        self.set(1, 0)
        self.set(0, 0)

    def rs(self):
        self.set(0, 1)
        self.set(1, 1)
        self.set(1, 0)
        self.set(0, 0)

    def stop(self):
        self.set(0, 0)
        self.set(1, 0)
        self.set(1, 1)

    def bit(self, v):
        self.set(0, v)
        self.set(1, v)
        self.set(0, v)

    def byte(self, b):
        for i in range(7, -1, -1):
            self.bit((b >> i) & 1)

    def push(self, byte=0, start=0, stop=0, read=0, rcont=0):
        self.row({'push': 1, 'byte': byte, 'start': start, 'stop': stop, 'read': read, 'rcont': rcont, 'nak_ok': 0})

    def pop(self, byte=0, start=0, stop=0, read=0, rcont=0):
        self.row(None, valid=1, ready=1, fmt_byte=byte, fmt_start=start, fmt_stop=stop, fmt_read=read, fmt_rcont=rcont)

    def rx(self, b):
        self.row(None, rx_valid=1, rx_data=b)

    def reset(self):
        self.row({'rst_n': 0})


def txn(g, reads, data, rxfn=None, ackfn=None, early_pop=False, stretch=False, end='stop', cut=None, nsend=None, addr=0xA1):
    g.push(byte=addr, start=1)
    for fb, rc, sp in reads:
        g.push(byte=fb, read=1, rcont=rc, stop=sp)
    g.start()
    g.byte(addr)
    g.bit(0)
    g.pop(byte=addr, start=1)
    k = 0
    for fb, rc, sp in reads:
        n = fb or 256
        if early_pop:
            g.pop(byte=fb, read=1, rcont=rc, stop=sp)
        for j in range(n if nsend is None else nsend):
            b = data[k % len(data)]
            if stretch and k == 0:
                for _ in range(3):
                    g.row({'stretch': 1}, scl=0, scl_pin=1)
            g.byte(b)
            for x in (rxfn(k, b) if rxfn else [b]):
                g.rx(x)
            a = 0 if (j < n - 1 or rc) else 1
            if ackfn:
                a = ackfn(k, a)
            g.bit(a)
            k += 1
            if cut is not None and k >= cut:
                return
        if not early_pop:
            g.pop(byte=fb, read=1, rcont=rc, stop=sp)
    if end == 'stop':
        g.stop()


def run(check_rows):
    D = [0x5A, 0xC3, 0x0F, 0xF0]
    out = []

    def fams(r):
        return [e['family'] for e in r['events']]

    def cats(r):
        return [f['category'] for f in r['failures']]

    def add(name, ok):
        out.append({'name': name, 'pass': bool(ok)})

    def mk(reads, **kw):
        g = G()
        txn(g, reads, kw.pop('data', D), **kw)
        return check_rows(g.rows)

    r = mk([(3, 0, 1)])
    add('clean_multi_byte_read_pass', r['verdict'] == 'pass' and 'multi_byte_read' in fams(r) and 'read_stretch_recovery' not in fams(r))
    r = mk([(3, 0, 1)], rxfn=lambda k, b: [b ^ 1] if k == 1 else [b])
    add('rx_corruption_fails', r['verdict'] == 'fail' and 'rx_data' in cats(r) and not r['events'])
    r = mk([(3, 0, 1)], rxfn=lambda k, b: [b, b] if k == 0 else [b])
    add('rx_duplicate_fails', r['verdict'] == 'fail' and 'extra_rx' in cats(r) and not r['events'])
    r = mk([(3, 0, 1)], rxfn=lambda k, b: [] if k == 2 else [b])
    add('rx_missing_fails', r['verdict'] == 'fail' and 'missing_rx' in cats(r) and not r['events'])
    r = mk([(3, 0, 1)], ackfn=lambda k, a: 1 if k == 0 else a)
    add('intermediate_nack_fails', r['verdict'] == 'fail' and 'read_ack' in cats(r))
    r = mk([(3, 0, 1)], ackfn=lambda k, a: 0 if k == 2 else a)
    add('final_ack_without_rcont_fails', r['verdict'] == 'fail' and 'read_ack' in cats(r))
    r = mk([(2, 1, 0), (2, 0, 1)])
    add('rcont_chain_pass', r['verdict'] == 'pass' and 'rcont_chain' in fams(r))
    r = mk([(2, 1, 0), (2, 0, 1)], ackfn=lambda k, a: 1 if k == 1 else a)
    add('rcont_boundary_nack_fails', r['verdict'] == 'fail' and 'read_ack' in cats(r) and not r['events'])
    r = mk([(0, 0, 1)], data=list(range(256)))
    add('fbyte0_reads_256_pass', r['verdict'] == 'pass' and r['counts']['rx'] == 256 and 'multi_byte_read' in fams(r))
    r = mk([(0, 0, 1)], nsend=2)
    add('fbyte0_truncated_fails', r['verdict'] == 'fail' and 'premature_pop' in cats(r))
    r = mk([(3, 0, 1)], early_pop=True)
    add('premature_pop_fails', r['verdict'] == 'fail' and 'premature_pop' in cats(r))
    g = G()
    txn(g, [(3, 0, 1)], D, cut=1)
    g.reset()
    txn(g, [(2, 0, 1)], D)
    r = check_rows(g.rows)
    add('reset_separates_transactions_pass', r['verdict'] == 'pass' and len(r['events']) == 1)
    g = G()
    txn(g, [(3, 0, 1)], D, cut=1, rxfn=lambda k, b: [])
    g.reset()
    g.rx(D[0])
    r = check_rows(g.rows)
    add('stale_rx_after_reset_fails', r['verdict'] == 'fail' and 'extra_rx' in cats(r))
    r = mk([(3, 0, 1)], cut=1)
    add('incomplete_is_pending_no_event', r['verdict'] == 'pending' and not r['events'])
    g = G()
    txn(g, [(2, 0, 0)], D, end='none')
    g.push(byte=0xA0, start=1)
    g.push(byte=0x55, stop=1)
    g.rs()
    g.byte(0xA0)
    g.bit(0)
    g.pop(byte=0xA0, start=1)
    g.byte(0x55)
    g.bit(0)
    g.pop(byte=0x55, stop=1)
    g.stop()
    r = check_rows(g.rows)
    add('read_then_restart_pass', r['verdict'] == 'pass' and 'read_then_restart' in fams(r))
    r = mk([(3, 0, 1)], stretch=True)
    add('read_stretch_recovery_pass', r['verdict'] == 'pass' and 'read_stretch_recovery' in fams(r))
    r = mk([(3, 0, 1)], stretch=True, rxfn=lambda k, b: [b ^ 0x80] if k == 0 else [b])
    add('stretch_with_bad_rx_no_credit', r['verdict'] == 'fail' and not r['events'])
    return out

