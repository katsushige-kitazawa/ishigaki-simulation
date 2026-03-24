# 石垣島 社会シミュレーション — シナリオ設定ファイル

> UIの ⚙️ 設定パネルから変更するか、このファイルを直接編集して「📂 読み込む」でUIに反映できます。
> 設定は `config` コードブロック内の JSON を編集してください。

```json
{
  "scenario_name": "石垣島 春の観光シーズン",
  "date": "2026-03-23",
  "day_of_week": "月曜日",
  "weather": {
    "condition": "晴れ",
    "temperature": 25,
    "wind": "南風"
  },
  "season": "春",
  "agents": {
    "locals": 12,
    "migrants": 6,
    "tourists": 12
  },
  "special_events": [
    "川平湾シュノーケルツアー開催中",
    "公設市場は朝8時から営業",
    "離島ターミナル近くで夕日が美しい"
  ],
  "economy": {
    "tourism_level": "high",
    "fishing_conditions": "良好",
    "accommodation_rate": 0.85
  },
  "hazard_display": {
    "tsunami": false,
    "flood": false,
    "sediment": false
  },
  "notes": "春の観光シーズン。本土からの観光客が増加している時期。漁業者は観光ボートの増加による漁場への影響を懸念。移住者と地元民のコミュニティ関係も変化しつつある。"
}
```

---

## フィールド説明

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `scenario_name` | string | シナリオの名称 |
| `date` | string (YYYY-MM-DD) | シミュレーション日付 |
| `day_of_week` | string | 曜日（表示用） |
| `weather.condition` | string | 天気（晴れ / 曇り / 雨 / 台風） |
| `weather.temperature` | number | 気温 (℃) |
| `weather.wind` | string | 風の説明 |
| `season` | string | 季節（春 / 夏 / 秋 / 冬） |
| `agents.locals` | number | 表示する地元民の人数 (0〜12) |
| `agents.migrants` | number | 表示する移住者の人数 (0〜6) |
| `agents.tourists` | number | 表示する観光客の人数 (0〜12) |
| `special_events` | array | 当日の特別イベントリスト |
| `economy.tourism_level` | string | 観光度 (low / medium / high) |
| `economy.fishing_conditions` | string | 漁業状況 |
| `economy.accommodation_rate` | number | 宿泊施設稼働率 (0.0〜1.0) |
| `hazard_display.tsunami` | boolean | 津波浸水想定区域を表示するか |
| `hazard_display.flood` | boolean | 洪水浸水想定区域を表示するか |
| `hazard_display.sediment` | boolean | 土砂災害警戒区域を表示するか |
| `notes` | string | シナリオの補足説明 |

---

## シナリオのカスタマイズ例

### 例1: 台風接近シナリオ
```json
{
  "scenario_name": "台風接近時の避難行動",
  "weather": { "condition": "台風", "temperature": 28, "wind": "北東・強風" },
  "agents": { "locals": 12, "migrants": 6, "tourists": 4 },
  "hazard_display": { "tsunami": true, "flood": true, "sediment": true }
}
```

### 例2: 夏の観光ピークシナリオ
```json
{
  "scenario_name": "夏のハイシーズン",
  "date": "2026-08-15",
  "weather": { "condition": "晴れ", "temperature": 32, "wind": "南東" },
  "agents": { "locals": 12, "migrants": 6, "tourists": 12 },
  "economy": { "tourism_level": "high", "accommodation_rate": 0.98 }
}
```

### 例3: 閑散期シナリオ
```json
{
  "scenario_name": "冬の閑散期",
  "date": "2026-01-20",
  "weather": { "condition": "曇り", "temperature": 18, "wind": "北風" },
  "agents": { "locals": 12, "migrants": 6, "tourists": 3 },
  "economy": { "tourism_level": "low", "accommodation_rate": 0.35 }
}
```
