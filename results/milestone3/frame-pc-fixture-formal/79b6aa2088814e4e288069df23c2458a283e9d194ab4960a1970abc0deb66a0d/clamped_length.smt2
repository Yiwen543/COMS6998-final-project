; benchmark generated from python API
(set-info :status unknown)
(declare-fun h_original_length () (_ BitVec 16))
(declare-fun h_length () (_ BitVec 16))
(declare-fun h_valid () Bool)
(declare-fun rst () Bool)
(assert
 (let (($x83 (and (and (bvuge h_original_length (_ bv4 16)) (bvule h_original_length (_ bv8 16))) (and (distinct h_length h_original_length) true))))
(let (($x103 (or (and (bvugt h_original_length (_ bv8 16)) (and (distinct (_ bv8 16) h_length) true)) $x83)))
(let (($x62 (or (and (bvult h_original_length (_ bv4 16)) (and (distinct (_ bv4 16) h_length) true)) $x103)))
(let (($x79 (and (and (not rst) h_valid) $x62)))
(xor $x79 $x79))))))
(check-sat)
