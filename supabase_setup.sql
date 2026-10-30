-- 回收吧！債券火箭：排行榜資料表
-- 用法：Supabase 後台 → 左邊 SQL Editor → New query → 整段貼上 → 按 Run（只要做一次）

create table if not exists public.rocket_scores (
  id             bigint generated always as identity primary key,
  board_id       text        not null,                       -- 哪一期的排行榜（app.py 的 BOARD_ID）
  name           text        not null check (char_length(name) between 1 and 12),
  score          integer     not null check (score between 0 and 10000),  -- 遊戲最高約 8,300 分，超過就是作弊
  bond           text,                                       -- 這趟飛的債券
  mission_rating text,                                       -- 任務評等 AAA / A / BBB / BB / D / 落海
  created_at     timestamptz not null default now()
);

create index if not exists rocket_scores_board_score_idx
  on public.rocket_scores (board_id, score desc);

-- 開啟 RLS：玩家只能「看」和「新增」，不能改或刪別人的成績
alter table public.rocket_scores enable row level security;

drop policy if exists "rocket read"   on public.rocket_scores;
drop policy if exists "rocket insert" on public.rocket_scores;

create policy "rocket read"   on public.rocket_scores for select to anon using (true);
create policy "rocket insert" on public.rocket_scores for insert to anon with check (true);

-- ===== 之後管理用（需要時再單獨執行）=====
-- 看某一期前 20 名：
--   select name, max(score) as best from rocket_scores where board_id = 'rocket-2026-11'
--   group by name order by best desc limit 20;
-- 刪掉測試成績：
--   delete from rocket_scores where board_id = 'rocket-2026-11' and name = '測試';
