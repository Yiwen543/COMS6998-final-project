always @* check_bundled: assert(!(active && (valid_lost || (data_changed || (last_changed || user_changed)))));
