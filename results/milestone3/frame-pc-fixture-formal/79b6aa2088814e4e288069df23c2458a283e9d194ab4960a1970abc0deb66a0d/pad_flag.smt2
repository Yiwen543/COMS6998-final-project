; benchmark generated from python API
(set-info :status unknown)
(declare-fun h_original_length () (_ BitVec 16))
(declare-fun h_pad () Bool)
(declare-fun h_valid () Bool)
(declare-fun rst () Bool)
(assert
 (let (($x69 (and (and (not rst) h_valid) (xor h_pad (bvult h_original_length (_ bv4 16))))))
(xor $x69 $x69)))
(check-sat)
