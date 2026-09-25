# 證據與步驟記錄

此模板只記錄可核對的工作事實，不要求內部思考逐字稿。可直接放在任務筆記、issue、PR 描述或對話中。

## 任務級記錄

```text
TASK
- Request:
- Deliverable:
- Target/version/time scope:
- Allowed side effects:
- Applicable project rules:
```

## 每步開始前

```text
STEP <N>
G1 SOURCE / SPEC
- Source:
- Version/date:
- Exact section read:
- Supports:
- Unknown/conflict:

G2 CURRENT STATE
- Target read:
- Relevant implementation/data/tests read:
- Current diff/state:
- Proven gap:

G3 STEP CONTRACT
- Single purpose:
- Allowed files/resources:
- Maximum scope:
- Invariants:
- Operation/command:
- Validation:
- Stop conditions:
- Recovery:
```

必要欄位未知時標記 `BLOCKED`，先補證據；不得先操作再回填。

## 每步操作後

```text
G4 OBSERVED CHANGE
- Actual operation:
- Actual files/resources changed:
- Diff/output inspected:
- Unexpected effects:

G5 VALIDATION
- Check:
- Result: PASS | FAIL | NOT RUN
- Evidence/output:
- Remaining limitation:
```

## 最終交付

```text
G6 DELIVERY
- Completed:
- Validation actually run:
- NOT RUN:
- Remaining blockers/limitations:
- Final changed files/resources:
- Sources used:
```

`PASS` 只能來自實際完成的檢查；預期結果、自填文字、口頭表示「應該沒問題」不能當成 PASS。
