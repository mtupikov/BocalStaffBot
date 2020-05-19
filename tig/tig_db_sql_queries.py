tig_db_name = 'tig_db.sqlite'
tig_table = 'tig_table'
create_tig_table_query = f'create table if not exists {tig_table} (' \
                            f'username text,' \
                            f'user_id integer,' \
                            f'reason text,' \
                            f'current_tig_date text,' \
                            f'is_active boolean' \
                            f')'
insert_tig_query = f'insert into {tig_table} values (?, ?, ?, ?, ?)'
select_all_tig_list = f'select * from {tig_table}'
select_tig_list_by_id = f'select * from {tig_table} where user_id=?'
select_active_tig_list_by_id = f'select * from {tig_table} where user_id=? and is_active=true'
select_active_tig_list = f'select * from {tig_table} where is_active=true'
update_inactive_query = f'update {tig_table} set is_active=false where user_id=?'
update_user_tig_query = f'update {tig_table} set is_active=true,' \
                            f'reason=?,' \
                            f'current_tig_date=?' \
                            f'where user_id=?'
