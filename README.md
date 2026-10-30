# 回收吧！債券火箭 — 排行榜版部署說明

## 資料夾裡有什麼

| 檔案 | 用途 |
|---|---|
| `app.py` | Streamlit 主程式，負責把遊戲放滿整個畫面、接上排行榜 |
| `game.html` | 遊戲本體（3D 火箭、選債、條件書、排行榜畫面都在這裡） |
| `requirements.txt` | 告訴 Streamlit Cloud 要裝什麼套件 |
| `supabase_setup.sql` | 建排行榜資料表，只要執行一次 |
| `.streamlit/secrets.toml.example` | Secrets 範本，看格式用，不用上傳 |

## 第一次部署（大約 10 分鐘）

### 步驟 1：在 Supabase 建排行榜資料表
1. 登入 Supabase，進到你放遊戲成績的那個專案（就是債速配用的那個，不是債券群島的）。
2. 左邊選 **SQL Editor** → **New query**。
3. 打開 `supabase_setup.sql`，全部複製貼上，按 **Run**。看到 Success 就完成了。

### 步驟 2：找出兩個連線資料
1. Supabase 左邊選 **Project Settings** → **API**（新版在 **API Keys**）。
2. 抄下 **Project URL**（長得像 `https://xxxx.supabase.co`）。
3. 抄下 **anon public** 那一把金鑰。
   - ⚠️ 不要用 **service_role**。那把有完整權限，放進遊戲等於把資料庫鑰匙交給所有玩家。

### 步驟 3：上傳到 GitHub
1. GitHub 新開一個 repo，例如 `bond-rocket`（Public 即可，金鑰不會放在程式碼裡）。
2. 把 `app.py`、`game.html`、`requirements.txt` 三個檔案上傳。
   - `supabase_setup.sql`、`README.md` 要不要上傳都可以。
   - **不要**上傳真正的 `secrets.toml`。

### 步驟 4：在 Streamlit Cloud 開 app
1. Streamlit Cloud → **Create app** → 選剛剛的 repo，Main file 填 `app.py`。
2. 開進階設定 **Advanced settings** → **Secrets**，貼上：
   ```toml
   SUPABASE_URL = "https://你的專案.supabase.co"
   SUPABASE_ANON_KEY = "你的 anon public 金鑰"
   ```
3. 按 **Deploy**。等一兩分鐘就有公開網址。

### 步驟 5：測一下
1. 打開網址，主畫面應該會出現「看排行榜」按鈕（沒出現代表 Secrets 沒讀到）。
2. 飛一趟、答完加碼題、輸入名字按「登上排行榜」。
3. 測完想刪掉測試成績，到 SQL Editor 執行 `supabase_setup.sql` 最下面那段 delete。

## 之後常做的事

### 換一批熱銷券
打開 `game.html`，搜尋 `債券資料：換券只要改這一段`，照格式改 `PRICE_DATE` 和 `BONDS` 裡的每一檔：

```js
{code:'WMBB26070003',name:'輝達公司債11',ytm:5.45,ytc:5.46,offer:96.32,cpn:4.95,freq:'每半年',
 mat:'2036/6/15',yrs:9.63,rating:'AA',rank:'優先無擔保',risk:'P1',min:'USD 2,000',call:'Make Whole Call'},
```

- `ytc` 沒有就填 `null`。
- 沒有 S&P 評等就填 `'NA'`。
- 火箭性能（風暴、配息、落地標準、分數加權）會依條件自動算，不用另外調。
- 改完存檔、上傳覆蓋 GitHub 上的 `game.html`，Streamlit 會自動更新。

### 開新一期排行榜
打開 `app.py`，把 `BOARD_ID = "rocket-2026-11"` 改成新名字（例如 `"rocket-2026-12"`）。舊成績還在資料庫，只是新的一期從零開始。

### 加到投資機長箱
在入口網站新增一張卡片，連到這個 app 的網址即可。

## 遊戲規則對照（給同仁看的說明）

| 債券條件 | 遊戲裡的效果 |
|---|---|
| 票面利率 | 配息金幣每顆補回的本金（票面 × 2.4%） |
| 剩餘年期 | 升息風暴的推力；超過 25 年風暴 3 次 |
| S&P 評等 | 落地標準：評等越好越寬鬆；NA 為一般標準 |
| 債券順位 | 次順位的落地標準再嚴一點 |
| YTM | 分數加權（以本期最低 YTM 為 ×1.00） |

> 僅供內部教育訓練使用，請勿外流，非投資建議。
