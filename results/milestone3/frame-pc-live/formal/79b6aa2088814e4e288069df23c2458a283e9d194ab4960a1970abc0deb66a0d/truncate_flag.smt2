; benchmark generated from python API
(set-info :status unknown)
(declare-fun h_original_length () (_ BitVec 16))
(declare-fun h_truncate () Bool)
(declare-fun h_valid () Bool)
(declare-fun rst () Bool)
(assert
 (let (($x83 (and (and (not rst) h_valid) (xor h_truncate (bvugt h_original_length (_ bv8 16))))))
(xor $x83 $x83)))
(check-sat)
