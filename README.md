# evidence-first-knowledge-work

知識型任務的行為規範 Skill，採繁體中文，版本 1.0.0。

核心要求：先查後寫；每個編輯步驟前重讀相符版本文件及目標現況；證據不足時停止該步；只宣稱實際驗證過的結果。

## 內容

| 檔案 | 用途 |
| --- | --- |
| [SKILL.md](SKILL.md) | 必須完整載入的核心原則、G0–G6 關卡、逐步重查、阻擋與交付規則。 |
| [references/coding-protocol.md](references/coding-protocol.md) | 倉庫盤點、API 核對、修改契約、命令、副作用、測試與精準回退。 |
| [references/knowledge-protocol.md](references/knowledge-protocol.md) | 研究、原文閱讀、分析、引用及文件維護。 |
| [references/evidence-template.md](references/evidence-template.md) | 精簡證據與每步操作前後記錄。 |
| [references/acceptance-cases.md](references/acceptance-cases.md) | 20 個行為驗收情境；檢查實際操作順序及證據。 |
| [AGENTS.snippet.md](AGENTS.snippet.md) | Codex 專案常駐載入規則，合併到既有 AGENTS.md。 |
| [CLAUDE.snippet.md](CLAUDE.snippet.md) | Claude Code 專案常駐載入規則，合併到既有 CLAUDE.md。 |
| [LICENSE](LICENSE) | MIT 開源授權。 |

## 安裝與載入

本包只提供檔案，沒有自動安裝、執行攔截器或修改使用者設定的程式。

### Codex 專案

將整個資料夾放在專案的 `.agents/skills/evidence-first-knowledge-work/`。Codex 官方文件列出此類專案 skills 位置，並說明明確點名與依描述匹配兩種使用方式。[1]

先閱讀既有 `AGENTS.md` 及適用規則，再將 `AGENTS.snippet.md` 整合進根目錄 `AGENTS.md`，保留原有內容，避免重複條款。Codex 在啟動時建立指令鏈；合併後開啟新工作階段，檢查實際載入位置、覆寫檔與容量限制。[2]

可在任務中明確點名：[1]

```text
$evidence-first-knowledge-work
依此規範執行本次任務，先完成查證與編輯前閱讀。
```

### Claude Code 專案

將整個資料夾放在專案的 `.claude/skills/evidence-first-knowledge-work/`，再讀取既有 `CLAUDE.md`，把 `CLAUDE.snippet.md` 整合其中，保留原有規則。[3][4]

可在任務中明確呼叫：[3]

```text
/evidence-first-knowledge-work
```

常駐指令與 Skill 的全文載入有不同作用，安裝後需檢查實際生效來源。此處提供兩種平台的專案用法；不用兩份摘要同時重複要求同一套規則。[2][4][5]

### 路徑與既有規範

摘要內使用專案根目錄相對路徑。採用其他安裝位置時，必須將摘要改成已確認存在的實際路徑，再檢查能否讀取；不能只搬移 Skill 而留下失效引用。

此包保留倉庫盤點、責任層與修改契約的工作方式，並加入跨任務與逐步查證關卡。若專案已另有相同規範，依有效授權整合、去重；不擅自刪除、停用或降低既有要求。

## 強制性的界線

Skill 與常駐指令可以明定「必須」「禁止」「未通過即停止」。本包未安裝任何外部工具攔截器，不能從系統層保證代理永遠遵守，也沒有宣稱已達成工具呼叫的硬性封鎖。

Claude 官方將 CLAUDE.md 定義為上下文中的行為指引，並區分工具 hook／受管設定等外部強制機制。單靠文字載入不能推定嚴格遵守。[4]

本包維持通用的指令型範圍，不臆造跨平台通用的強制 YAML 欄位、hook API 或權限設定。[6]

## 檢查方式與限制

格式檢查應確認 UTF-8、YAML 前置資料、name 與目錄一致、必要檔案及相對引用；壓縮包另檢查可讀取與內容完整性。[6]

行為檢查依 `references/acceptance-cases.md`，觀察來源讀取是否早於依賴它的撰寫／修改、修改範圍與驗證結果是否符合契約。格式合格、自填 PASS 與口頭表示理解，都不能證明代理已遵守。

未在使用者的 Codex、Claude Code 或其他代理環境進行載入測試或模型行為評測，未量測觸發率、遵守率或指令衝突時的行為。

## 官方格式與平台依據

查核日期：2026-09-25。以下來源用於檔案格式與載入方式；G0–G6 及具體工作限制是本包建立的行為規範，不代表平台官方政策。

[1] OpenAI，Using skills to accelerate OSS maintenance。Codex repo-local `.agents/skills/`、`AGENTS.md` 與漸進載入。

```text
https://developers.openai.com/blog/skills-agents-sdk
```

[2] OpenAI，Model guidance：Using AGENTS.md。Codex 的 AGENTS.md 載入與作用範圍。

```text
https://developers.openai.com/api/docs/guides/latest-model
```

[3] Anthropic，Explore the `.claude` directory。Claude Code 的 `.claude/skills/` 與 `CLAUDE.md` 位置。

```text
https://code.claude.com/docs/en/claude-directory
```

[4] Anthropic，Extend Claude Code。`CLAUDE.md`、Skills、Hooks 與權限機制的角色區分。

```text
https://code.claude.com/docs/en/features-overview
```

[5] Anthropic，Extend Claude Code。常駐指令與按需 Skill 的載入差異。

```text
https://code.claude.com/docs/en/features-overview
```

[6] Agent Skills，Specification。name、description、目錄、前置資料及相對引用。

```text
https://agentskills.io/specification
```
