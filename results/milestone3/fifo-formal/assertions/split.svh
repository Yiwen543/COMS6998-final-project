always @* check_valid_lost: assert(!(active && valid_lost));
always @* check_data_changed: assert(!(active && data_changed));
always @* check_last_changed: assert(!(active && last_changed));
always @* check_user_changed: assert(!(active && user_changed));
