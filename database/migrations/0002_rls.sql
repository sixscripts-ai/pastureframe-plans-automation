-- Optional Phase 2 RLS hardening. Apply only after the operator UI exists.
-- Default Postgres user (Supabase service role) bypasses RLS.

alter table products enable row level security;
alter table listing_metadata enable row level security;
alter table orders enable row level security;
alter table customer_messages enable row level security;
alter table content_tasks enable row level security;
alter table reviews enable row level security;
alter table weekly_reports enable row level security;
alter table compliance_log enable row level security;
alter table automation_runs enable row level security;

-- Operator role (granted to Ashton's Supabase Auth user) gets full read.
create policy operator_read_all on products
  for select using (auth.role() = 'authenticated');
-- Repeat similar policies per table as the UI is built.
