-- =====================================================================
-- PastureFrame Plans Automation — Database Schema (Supabase / Postgres)
-- =====================================================================
-- Apply via Supabase migration: see database/migrations/0001_init.sql
-- All buyer identifiers are STORED HASHED. Never store raw buyer email.
-- =====================================================================

create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";

-- =====================================================================
-- 1. PRODUCTS
-- =====================================================================
create table if not exists products (
  product_id              uuid primary key default uuid_generate_v4(),
  slug                    text unique not null,
  product_name            text not null,
  product_type            text not null check (product_type in (
    'mobile_coop','garden_shade_roof','raised_bed','broiler_tractor',
    'layer_coop','duck_tractor','rabbit_tractor','goat_shelter',
    'bundle','worksheet'
  )),
  status                  text not null default 'draft' check (status in (
    'idea','draft','ready_for_review','approved_for_listing',
    'listed','retired'
  )),
  version                 text not null default '1.0.0',
  price                   numeric(10,2),
  target_customer         text,
  description             text,
  disclaimer              text,
  product_folder_url      text,
  etsy_listing_id         bigint,
  etsy_listing_status     text,
  created_at              timestamptz not null default now(),
  updated_at              timestamptz not null default now()
);
create index if not exists idx_products_status on products (status);

-- =====================================================================
-- 2. LISTING_METADATA
-- =====================================================================
create table if not exists listing_metadata (
  listing_id              uuid primary key default uuid_generate_v4(),
  product_id              uuid not null references products(product_id) on delete cascade,
  title                   text not null,                 -- Etsy 140 char max
  description             text not null,
  tags                    text[] not null default '{}',  -- max 13 tags
  category                text,
  taxonomy_id             bigint,
  price                   numeric(10,2) not null,
  quantity                integer not null default 999,
  digital_file_names      text[] not null default '{}',
  image_file_names        text[] not null default '{}',
  seo_score               integer,
  compliance_status       text not null default 'pending' check (
    compliance_status in ('pending','passed','failed','waived')
  ),
  approval_status         text not null default 'pending' check (
    approval_status in ('pending','approved','rejected','revision_requested')
  ),
  last_published_at       timestamptz,
  created_at              timestamptz not null default now(),
  updated_at              timestamptz not null default now(),
  constraint listing_tags_max_13 check (cardinality(tags) <= 13),
  constraint listing_title_max_140 check (char_length(title) <= 140)
);
create index if not exists idx_listing_product on listing_metadata (product_id);
create index if not exists idx_listing_approval on listing_metadata (approval_status);

-- =====================================================================
-- 3. ORDERS  (buyer ids stored hashed)
-- =====================================================================
create table if not exists orders (
  order_id                uuid primary key default uuid_generate_v4(),
  etsy_receipt_id         bigint unique not null,
  buyer_id_hash           text not null,                 -- sha256(buyer_user_id || salt)
  buyer_name_optional     text,
  purchase_date           timestamptz not null,
  product_ids             uuid[] not null default '{}',
  order_total             numeric(10,2) not null,
  order_status            text not null,                 -- mirrors Etsy receipt status
  fulfillment_status      text not null default 'digital_auto' check (
    fulfillment_status in ('digital_auto','manual_followup','issue')
  ),
  issue_status            text,
  notes                   text,
  created_at              timestamptz not null default now()
);
create index if not exists idx_orders_purchase_date on orders (purchase_date desc);

-- =====================================================================
-- 4. CUSTOMER_MESSAGES
-- =====================================================================
create table if not exists customer_messages (
  message_id              uuid primary key default uuid_generate_v4(),
  order_id                uuid references orders(order_id) on delete set null,
  buyer_id_hash           text not null,
  message_text_redacted   text not null,                 -- PII redacted
  detected_intent         text not null check (detected_intent in (
    'download_help','product_clarification','materials_question',
    'refund_request','complaint','safety_concern','custom_design',
    'legal_threat','harassment_spam','positive_feedback','review_issue',
    'other'
  )),
  sentiment               text check (sentiment in ('positive','neutral','negative')),
  risk_level              text not null check (risk_level in ('low','medium','high')),
  suggested_response      text,
  approval_required       boolean not null default true,
  approval_status         text not null default 'pending' check (
    approval_status in ('pending','approved','rejected','auto_sent')
  ),
  response_sent           boolean not null default false,
  created_at              timestamptz not null default now()
);
create index if not exists idx_msg_risk on customer_messages (risk_level);
create index if not exists idx_msg_approval on customer_messages (approval_status);

-- =====================================================================
-- 5. CONTENT_TASKS
-- =====================================================================
create table if not exists content_tasks (
  task_id                 uuid primary key default uuid_generate_v4(),
  product_id              uuid references products(product_id) on delete cascade,
  task_type               text not null check (task_type in (
    'product_outline','materials_list','cut_list','listing_copy',
    'listing_tags','image_brief','faq','marketing_pinterest',
    'marketing_blog','marketing_instagram','marketing_email',
    'compliance_review','improvement_recommendations'
  )),
  input_prompt            text not null,
  output_text             text,
  status                  text not null default 'queued' check (
    status in ('queued','running','completed','failed','approved','rejected')
  ),
  reviewer                text,
  created_at              timestamptz not null default now(),
  completed_at            timestamptz
);
create index if not exists idx_tasks_status on content_tasks (status);

-- =====================================================================
-- 6. REVIEWS
-- =====================================================================
create table if not exists reviews (
  review_id               uuid primary key default uuid_generate_v4(),
  order_id                uuid references orders(order_id) on delete set null,
  rating                  integer check (rating between 1 and 5),
  review_text             text,
  product_id              uuid references products(product_id) on delete set null,
  response_needed         boolean not null default false,
  suggested_response      text,
  approval_status         text not null default 'pending' check (
    approval_status in ('pending','approved','rejected','sent')
  ),
  created_at              timestamptz not null default now()
);

-- =====================================================================
-- 7. WEEKLY_REPORTS
-- =====================================================================
create table if not exists weekly_reports (
  report_id               uuid primary key default uuid_generate_v4(),
  week_start              date not null,
  week_end                date not null,
  revenue                 numeric(12,2),
  orders                  integer,
  conversion_rate         numeric(5,4),
  top_products            jsonb,
  issues                  jsonb,
  recommendations         jsonb,
  generated_at            timestamptz not null default now(),
  unique (week_start, week_end)
);

-- =====================================================================
-- 8. COMPLIANCE_LOG
-- =====================================================================
create table if not exists compliance_log (
  log_id                  uuid primary key default uuid_generate_v4(),
  event_type              text not null check (event_type in (
    'block','warn','pass','override','policy_review','disclosure'
  )),
  source_policy           text,                          -- e.g. 'etsy_seller_policy'
  system_area             text,                          -- 'listing','message','image','plan_copy'
  issue                   text not null,
  severity                text not null check (severity in ('low','medium','high','critical')),
  action_taken            text,
  approval_by             text,
  related_id              uuid,                          -- listing_id, message_id, etc.
  timestamp               timestamptz not null default now()
);
create index if not exists idx_compliance_severity on compliance_log (severity, timestamp desc);

-- =====================================================================
-- 9. AUTOMATION_RUNS
-- =====================================================================
create table if not exists automation_runs (
  run_id                  uuid primary key default uuid_generate_v4(),
  workflow_name           text not null,
  trigger                 text not null check (trigger in (
    'manual','cron','webhook','agent_chain'
  )),
  input_summary           text,
  output_summary          text,
  success                 boolean not null,
  error_message           text,
  duration_ms             integer,
  timestamp               timestamptz not null default now()
);
create index if not exists idx_runs_workflow on automation_runs (workflow_name, timestamp desc);
create index if not exists idx_runs_failures on automation_runs (success, timestamp desc) where success = false;

-- =====================================================================
-- updated_at trigger
-- =====================================================================
create or replace function set_updated_at() returns trigger language plpgsql as $$
begin new.updated_at := now(); return new; end $$;

drop trigger if exists trg_products_updated on products;
create trigger trg_products_updated before update on products
  for each row execute procedure set_updated_at();

drop trigger if exists trg_listing_updated on listing_metadata;
create trigger trg_listing_updated before update on listing_metadata
  for each row execute procedure set_updated_at();
