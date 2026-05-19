# AIDevHub 数据更新提示词

你是一个专业的开发者工具数据分析师。请根据最新的数据源更新 `/data` 目录下的JSON数据文件。

## 数据源

### 1. AI编程工具
- 来源: 官方产品页面、Product Hunt、GitHub
- 指标: 综合评分(1-10)、价格模式、开发商

### 2. 大模型编程能力
- 来源: https://www.datalearner.com/en/leaderboards/category/code
- 基准测试: SWE-bench Verified, LiveCodeBench, SWE-Bench Pro, Multilingual

### 3. 编程语言
- 来源: TIOBE指数, Stack Overflow调查, GitHub Octoverse
- 指标: 流行度评分

### 4. 数据库
- 来源: https://db-engines.com/en/ranking
- 分类: RDBMS, KV, Document, TimeSeries, Vector, Graph等

### 5. GitHub AI开源项目
- 来源: GitHub API搜索 `AI` 相关高star项目
- 分类: Agent, LLM, Image, Voice, Coding, RAG, Framework, Other
- 指标: Star数

## 数据格式要求

### tools.json
```json
[
  {
    "id": 1,
    "name": "工具名称",
    "vendor": "开发商",
    "score": 9.5,
    "price": "freemium|paid|free",
    "colors": ["#color1", "#color2"],
    "tags": ["标签1", "标签2", "标签3"],
    "desc": "中文描述（包含数据源）",
    "desc_en": "English description",
    "website": "https://...",
    "icon": "https://logo.clearbit.com/domain.com"
  }
]
```

### models.json
```json
{
  "swe-bench": [
    {
      "id": 1,
      "name": "模型名称",
      "vendor": "开发商",
      "score": 93.9,
      "passRate": "93.9%",
      "colors": ["#color1", "#color2"],
      "desc": "中文描述（包含数据源: datalearner.com）",
      "desc_en": "English description",
      "icon": "https://logo.clearbit.com/domain.com"
    }
  ],
  "livecode": [...],
  "swe-pro": [...],
  "multilingual": [...]
}
```

### languages.json
```json
[
  {
    "id": 1,
    "name": "Python",
    "rank": 1,
    "score": 100.0,
    "type": "脚本语言",
    "colors": ["#color1", "#color2"],
    "desc": "中文描述（包含数据源）",
    "desc_en": "English description",
    "icon": "https://logo.clearbit.com/python.org"
  }
]
```

### databases.json
```json
{
  "rdbms": [
    {
      "id": 1,
      "name": "Oracle",
      "vendor": "Oracle",
      "score": 1143.28,
      "type": "商业关系型",
      "colors": ["#color1", "#color2"],
      "desc": "中文描述（包含数据源: db-engines.com）",
      "icon": "https://logo.clearbit.com/oracle.com"
    }
  ],
  "kv": [...],
  "document": [...],
  "timeseries": [...],
  "vector": [...],
  "graph": [...],
  "wideColumn": [...],
  "search": [...],
  "bigdata": [...]
}
```

### github.json
```json
[
  {
    "id": 1,
    "name": "项目名",
    "repo": "owner/repo",
    "stars": 184370,
    "desc": "项目描述（英文）",
    "language": "Python",
    "category": "Agent",
    "topics": ["ai", "agent"],
    "icon": "https://github.com/owner.png?size=64",
    "license": "MIT"
  }
]
```

## 注意事项

1. 图标URL使用 `https://logo.clearbit.com/{domain}` 格式
2. GitHub项目头像使用 `https://github.com/{owner}.png?size=64` 格式
3. 描述中必须包含数据来源
4. 保持中英文双语
5. 按要求更新 `lastUpdated` 时间戳

## 执行步骤

1. 读取现有JSON文件了解当前数据
2. 访问数据源获取最新数据
3. 合并更新数据，保持ID一致性
4. 验证JSON格式正确性
5. 更新文件并记录更新时间