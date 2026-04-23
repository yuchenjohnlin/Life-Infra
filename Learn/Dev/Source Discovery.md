# Source Discovery 的設計細節

## 一、評估來源的維度

你直覺對了——**先定清楚標準比直接丟 prompt 重要**。一個 topic 可能有上千筆結果，沒有篩選準則，Claude 只會給你搜尋引擎前幾名（那些通常是 SEO 優化過的內容農場）。

以下是我建議的六個維度，可以全部或挑幾個放進 skill：

**1. 權威性 (Authority)**

- 作者是不是該領域實際從業者？有沒有可驗證的經歷（GitHub、LinkedIn、公司 engineering blog）？
- 是不是第一手來源？官方文件 / 論文原作 / 從業者親述 > 二手整理 > 三手 listicle
- 例如搜 "harness engineer"，Harness.io 官方 blog 和真正在那邊工作過的人寫的文章權威性高，「Top 10 things about harness engineers」這種就低

**2. 熱度／社群驗證 (Traction)**

- YouTube：觀看數、按讚比例、留言有沒有認真討論（而不是「感謝大大」）
- 文章：Hacker News 分數、Twitter/X 的討論、Reddit 的引用
- GitHub repo：stars、近期的 commit 活躍度
- 注意：熱門不等於好。熱門只代表「很多人看過」，要跟權威性交叉參照

**3. 時效性 (Recency)**

- 分兩種 topic 處理：
    - **快變動類**（AI 工具、某個新框架、某公司動態）：需要近 6-12 個月的內容
    - **基礎概念類**（演算法、設計原則、角色職責）：老文章通常反而更好，已經被時間驗證

**4. 深度／難度層級 (Depth)**

- 給使用者選：入門 overview / 中階實作 / 深度原理 / 案例研究
- 好的來源組合通常是「一篇 overview + 一兩篇深度 + 一份 hands-on」的搭配，不是五篇都同一層

**5. 多樣性／互補性 (Diversity)**

- 格式多樣：影片、長文、官方文件、程式碼、討論串，各至少一份
- 觀點多樣：批評者的觀點 vs 擁護者的觀點
- 避免五筆都在講同一件事——這是 discovery 最容易踩的坑

**6. 信噪比 (Signal-to-noise)**

- 排除：AI 生成的內容農場、廣告式「比較文」、只有標題殺手沒內容的 Medium 文、「10 分鐘速成」課程
- 判斷訊號：是否有具體例子 / 實際數字 / 可運行的程式碼 / 親身經驗

## 二、Skill 的運作流程

我建議 skill 做成這幾步，不要只是「搜尋 → 給你 10 筆」：

**Step 1: 釐清主題（interview）**  
使用者輸入「harness engineer」，但這太模糊。skill 先問：

- 你想學到什麼程度？（認識這個角色 / 想轉職 / 想評估要不要導入他們家產品）
- 你的先備知識？（完全新手 / 熟 DevOps 但沒碰過 Harness）
- 有沒有語言偏好？
- 有沒有時間偏好？（只要近一年的 / 不限）

**Step 2: 分層搜尋**  
根據上面的答案，對每個維度分別下一組搜尋 query，不是一次性「harness engineer guide」完事。例如：

- `Harness.io engineering blog`（官方一手）
- `Harness CI/CD real world case study`（實戰）
- `site:news.ycombinator.com harness`（社群驗證）
- `harness vs argo vs jenkins 2026`（對比觀點）

**Step 3: 初篩＋打分**  
對抓回來的 20-30 筆，Claude 按你給的維度打分，剔掉明顯的內容農場，留下前 8-10 筆候選。

**Step 4: 比較矩陣**  
把最後候選排成一個表格寫進 Obsidian：每筆一列，欄位是來源類型、作者可信度、涵蓋角度、預估閱讀時間、獨特價值、與其他幾筆的重疊度。

**Step 5: 推薦組合**  
Claude 不只列清單，還給你「如果只有 1 小時，先看這 3 筆」的建議組合。

**Step 6: 等你的決策**  
最後一欄留空讓你打勾，打勾的才進 ingestion。