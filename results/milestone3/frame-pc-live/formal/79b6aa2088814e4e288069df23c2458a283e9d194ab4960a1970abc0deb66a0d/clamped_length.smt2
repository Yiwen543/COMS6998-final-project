; benchmark generated from python API
(set-info :status unknown)
(declare-fun h_original_length () (_ BitVec 16))
(declare-fun h_length () (_ BitVec 16))
(declare-fun h_valid () Bool)
(declare-fun rst () Bool)
(assert
 (let (($x70 (and (and (bvuge h_original_length (_ bv4 16)) (bvule h_original_length (_ bv8 16))) (and (distinct h_length h_original_length) true))))
(let (($x64 (or (and (bvugt h_original_length (_ bv8 16)) (and (distinct (_ bv8 16) h_length) true)) $x70)))
(let (($x45 (or (and (bvult h_original_length (_ bv4 16)) (and (distinct (_ bv4 16) h_length) true)) $x64)))
(let (($x106 (and (and (not rst) h_valid) $x45)))
(xor $x106 $x106))))))
(check-sat)
