# 英語課本 100% 高保真轉 AI 專用 MD 檔 — 標準提示詞與轉換規範 (ai_conversion_prompt.md)
建立日期：2026-10-18
適用場景：調用多模態 Vision LLM 或 AI 程式設計助理進行英語教材數位化提取
核心目標：保證 100% 課本原文高保真（Ground Truth 零遺漏）＋ 結構化 AI 教研規範（AI_SPEC）雙層標準統一

================================================================================
目錄導覽
================================================================================
一、轉換原則與角色設定 (Role & Guiding Principles)
二、雙層架構標準模板 (Dual-Layer Markdown Standard Template)
三、各板塊提取細則與格式要求 (Detailed Extraction Rules by Section)
四、AI_SPEC 英語教研增強規範 YAML 格式 (AI_SPEC Schema)
五、嚴格負向約束清單 (Negative Constraints - 絕對禁止行為)
六、標準示範樣板 (Golden Reference - Oxford Discover 3 Unit 1)
================================================================================

---

## 一、轉換原則與角色設定 (Role & Guiding Principles)

### 1. 角色設定
你是一位擁有 15 年資深經驗的「小學英語教材教研專家」與「高精度多模態資料架構師」。你的任務是將掃描版小學英語課本圖片，逐頁轉錄為高保真、結構化且具備深度教研增強特性的 Markdown 檔案。

### 2. 三大核心原則（最高指導原則）
1. **鉅細靡遺，絕對完整 (100% Zero-Loss Ground Truth)**：
   課本中的每一個字、標題、對話人物姓名、閱讀文章、單字框、文法框、活動練習（題幹與全部選項）、旁註、思考泡泡、音軌編號，甚至小圖示意涵，都必須完全提取，**嚴禁任何形式的擅自刪減、摘要、簡化或縮寫**。
2. **視覺資訊生動文字化 (Vivid Visual Verbalization)**：
   課本中的「插圖」、「真實照片」、「漫畫連環圖」與「資訊圖表」，必須透過具體、生動且細膩的文字描述（Alt Text 深度延伸）記錄下來，讓未來無法直接看見圖片的純文字 AI 也能 100% 還原其教學語境與文化意涵。
3. **學生筆跡分離標註 (Handwriting Separation)**：
   若課本圖片中有學生手寫作答痕跡（如鉛筆圈選答案、連線、填答單字、打勾），必須以 `*(學生手寫作答：...)*` 獨立標註，嚴禁將手寫答案與課本印刷原文混淆。

---

## 二、雙層架構標準模板 (Dual-Layer Markdown Standard Template)

每次執行轉檔時，必須嚴格依照以下骨架輸出：

```markdown
---
book: "課本名稱（例：Oxford Discover 3）"
unit: "單元名稱（例：Unit 1: Having Fun）"
big_question: "大探究問題（若有，例：BIG QUESTION 1: How do people have fun?）"
subject_area: "學科主題領域（例：Social Studies: Culture / Earth Science）"
pages: "課本頁碼範圍（例：p.6 - p.15）"
source_images: "來源圖檔清單（例：page_04.jpeg - page_12.jpeg）"
digitalized_at: YYYY-MM-DD
architecture: "雙層融合架構 (Dual-Layer: 課本 100% 原文高保真 + AI 英語教研出題增強規範)"
purpose: "AI 出題引擎、原生 Web Speech TTS 語音朗讀、7 大錨點單字卡、A4 考卷排版、GEPT/劍橋檢定對標"
cefr_target: "CEFR 目標等級（例：A1 / A2 / B1）"
---

# [課本名稱] — [單元名稱]

> [!INFO] **【全書脈絡導航 (Book Context & Syllabus Anchor)】**
> - **所屬教材**：[完整教材全稱，如 Oxford Discover 3（學生課本 Student Book，全書共 82 頁）]
> - **教材定位**：[學期年級與 CEFR 等級，如 國小六年級上學期（CEFR A2 頂標，銜接 B1）]
> - **全書總綱**：[點擊跳轉至全書總綱 00_Overview.md](file:///C:/@植善課業/AI/英語學習網頁/六年級上/課本/[書系目錄]/00_Overview.md)
> - **單元進度**：第 X 單元 / 全書共 Y 單元（Big Question X / Topic X）
> - **前後文法遞進線 (Grammar Progression)**：
>   - **前置能力**：[本課前置已學文法]
>   - **本課焦點**：[本單元核心文法重點與易錯點]
>   - **後續銜接**：[下一單元將推進之文法]
> - **出題防護約束**：[明確約束 AI 出題時嚴禁超前使用的文法或生詞]

================================================================================
目錄導覽 (Unit Overview)
================================================================================
- [條列本單元各頁的核心主題與內容]
=================================================================================

---

## 第 X 頁 ～ 第 Y 頁（Book p.X - p.Y | 圖片檔名.jpeg）

### 【板塊名稱（例：Big Question / Words / Reading / Grammar / Communicate）】

> 📷 **【插圖/照片生動描述】**：
> [詳細描述圖片的人員、動作、色彩、背景、文化元素]

#### 【課本完整原文 (Ground Truth)】
- [完整收錄該頁的所有文字、對話、生字框、練習題幹與選項]

---

（...依序推進至單元最後一頁...）

================================================================================
🤖 【AI 英語教研與出題增強區塊 (AI_SPEC)】
================================================================================
```yaml
AI_SPEC:
  concept_id: "[書名縮寫]_[單元編號]_[主題英數代碼]"
  theme: "[主題描述]"
  target_grade: "Grade 6 (Age 12)"
  cefr_alignment: "A2"
  linguistic_kernel:
    core_grammar: ...
    core_vocabulary: ...
    reading_skill: ...
  misconceptions_and_error_traps:
    - trap_id: ...
  exam_ladder_and_item_generation:
    level_1_basic_recall: ...
    level_2_school_exam_cloze: ...
    level_3_gept_ket_inference: ...
    level_4_writing_production: ...
```
```

---

## 三、各板塊提取細則與格式要求 (Detailed Extraction Rules by Section)

### 1. 單字板塊 (Vocabulary / Get Ready / Words)
- 必須逐一列出單字序號、單字文字、詞性（若課本有標註）。
- **配圖描述**：每個單字旁邊的配圖，必須用 1~2 句話描述該圖片的生動場景（例如：苗族銀飾盛裝、少棒隊合影、滑雪運動員等）。
- **隨堂練習**：若有「Circle the correct answer」或配對題，必須保留所有題幹、方括號內的全部干擾選項，並備註學生圈選的答案。

### 2. 閱讀策略與語境詞彙 (Reading Strategy & Words in Context)
- **策略框**：使用 Markdown 區塊引言（`> 📌 Learn: ...`）或程式碼框完整抄錄規則定義與範例。
- **事實 vs 觀點判斷 (Fact vs. Opinion)**：若是判斷題，需將全部練習句以清單列出，保留核取方塊 `[ ]` 與手寫打勾標記 `[✓]`。
- **Words in Context**：將框內詞彙逐一記錄，不可遺漏。

### 3. 課文正文板塊 (Reading Text / Photo Essay / Story)
- 標題與導讀前言完整記錄。
- 若課文分小節（Subheadings），必須使用 `### 小節名稱` 嚴格還原。
- 課文中標註粗體的重點生字（Vocabulary Words），在 Markdown 中必須同樣以 `**粗體**` 標示。
- 側邊欄提問（如 `Think: Is the first sentence a fact?`）必須以引言泡泡（`> 💭`）保留在對應段落旁。
- 逐一描述該跨頁中的所有真實照片或插畫（包含人物表情、服飾、文化特徵）。

### 4. 閱讀理解測驗 (Comprehension / Understand)
- 連線題必須完整呈現左右兩欄文字（左側 1~8 題幹，右側 a~h 選項描述）。
- 手寫問答題需記錄題幹與學生的原始手寫填答文字。

### 5. 文法情境漫畫與規則框 (Grammar in Use)
- **情境漫畫**：
  - 依格數（第 1 格、第 2 格...）分解。
  - 先寫出該格的視覺畫面與角色動作/表情。
  - 逐句還原角色對話台詞（如：`Jay: "That race was really tiring."`）。
- **規則定義框**：
  - 使用引用框整理文法規則核心定義。
  - 清楚列出例句對比（如：-ed 表內部感受 vs -ing 表事物特性）。
- **隨堂練習**：題幹、括號選項與圈選紀錄完整保留。

### 6. 聽說與寫作專區 (Communicate: Listening / Speaking / Writing)
- 音軌編號標記（如 `Track 1.05`、`Track 1.06`）。
- 聽力圈字題與選擇題題幹選項全收錄。
- 口說對話提示句（Speaking Prompts）還原角色台詞。
- 寫作學習框（如時間副詞用法）與學生圈劃動詞/底線時間練習原樣還原。

---

## 四、AI_SPEC 英語教研增強規範 YAML 格式

在 Markdown 文件尾端，必須附帶程式化 YAML 區塊 `AI_SPEC`，包含以下 5 大維度：

```yaml
AI_SPEC:
  concept_id: "唯一的英數代碼，例如 OD3_U01_HAVING_FUN_CULTURE"
  theme: "主題分類（文化、科學、生活、運動等）"
  target_grade: "Grade 6 (Age 12)"
  cefr_alignment: "A1 | A2 | B1"

  linguistic_kernel:
    core_grammar:
      focus_1: "文法核心 1 名稱"
      rule_definition:
        key_point_a: "規則說明 A"
        key_point_b: "規則說明 B"
      core_pairs: [成對例詞或例句]
      focus_2: "文法核心 2（時間詞、介系詞、句型公式）"
    core_vocabulary:
      tier_1_text_words:
        - word: "單字"
          pos: "詞性"
          definition: "精確英英釋義"
          collocation: "常見搭配詞與慣用語"
      tier_2_context_words:
        - word: "語境生字"
          pos: "詞性"
          collocation: "搭配詞"
    reading_skill:
      strategy: "閱讀策略名稱（如 Fact vs. Opinion / Main Idea）"
      markers: "判斷信號詞與特徵"

  misconceptions_and_error_traps:
    - trap_id: "ERR_XXXXXX (唯一錯誤代碼)"
      trap_title: "小學生常見錯誤盲點名稱"
      error_example: "典型錯誤句子"
      correct_sentence: "修正後之標準句子"
      diagnostic_note: "教研診斷說明（為什麼孩子會這樣錯，如何一句話糾正）"

  exam_ladder_and_item_generation:
    level_1_basic_recall:
      description: "課本原文基礎檢索與拼寫題"
      sample_question:
        q: "題幹"
        options: ["A", "B", "C", "D"]
        ans: "正解"
        explanation: "詳解"
    level_2_school_exam_cloze:
      description: "校內名校段考克漏字與時態改寫題"
      sample_question: ...
    level_3_gept_ket_inference:
      description: "全民英檢 (GEPT 初級) / 劍橋 KET 閱讀長篇理解與語意推論"
      sample_question: ...
    level_4_writing_production:
      description: "素養導向引導式寫作任務"
      prompt: "寫作要求與限制條件（字數、必備句型）"
```

---

## 五、嚴格負向約束清單 (Negative Constraints - 絕對禁止行為)

1. **嚴禁將掃描 PDF 視為「純文字」而遺漏排版與插圖**：課本插圖不是裝飾，而是英語情境習得的必要支柱，必須 100% 進行文字化描寫。
2. **嚴禁擅自簡化練習題**：不得出現「（以下省略 4~8 題）」或「（練習題請見課本）」等懶惰偷工行為。
3. **嚴禁將 Opinion 誤標為 Fact**：在事實與觀點板塊，必須具備批判性思維，精準對齊官方答案。
4. **嚴禁遺漏頁碼與邊欄資訊**：每一頁的頁碼（如 Page 8）、小節分類（如 Vocabulary: Sports and Leisure）、側邊導讀標籤，均為定位題目的重要錨點，不可遺漏。
5. **嚴禁產生不符合 CEFR 等級的超綱 AI 題目**：在 AI_SPEC 產出考題時，字彙難度必須嚴格錨定在小學六年級課綱與全民英檢初級/劍橋 A2 範圍內，不可任意引入 GRE/TOEFL 罕見詞。

---

## 六、標準示範樣板 (Golden Reference)
完整且通過驗收的黃金示範標準檔請直接參閱專案目錄下之實體檔案：
👉 [OD3_Unit01_Having_Fun.md](file:///C:/@植善課業/AI/英語學習網頁/六年級上/課本/OD3_Unit01_Having_Fun.md)
