# OpenCode Go 模型实测对比（2026-10-31）

订阅：OpenCode Go $10/月（Personal workspace）。37 个模型逐一实测。

## 方法

- **智力**：3 道硬题
  1. 递推：A缸10L、B空，每步 A半→B 再 B半→A，5次后 A=？（正确 `3415/512 ≈ 6.670`）
  2. 真假话：A:"B,C同类" B:"D,E不同" C:"A说谎" D:"B诚实" E:"C,D不同"（正确 `仅A`）
  3. 计数：lcm(a,b)=2³·3⁵·5² 的有序对数（正确 `385`）
- **速度**：定速任务（输出 1~100，约 200 token）端到端耗时，含 ~3s 客户端启动；~TPS 为估算
- Zen 试用模型配额约 1~3 次/17h（每模型独立），实测值

## 结果

| 模型 | 层级 | 月额度 | 题1 | 题2 | 题3 | 得分 | 定速耗时 | ~TPS | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| minimax-m3 | opencode-go | $60 | ✓ | ✓ | ✓ | **3/3** | 4.4s | ~144 | 最快档 |
| deepseek-v4.1-flash-free | opencode | Zen试用 | ✓ | ✓ | ✓ | **3/3** | 4.6s | ~124 | Zen试用配额 |
| glm-5.3-flash | opencode-go | $60 | ✓ | ✓ | ✓ | **3/3** | 5.9s | ~70 |  |
| glm-5.2 | opencode-go | $60 | ✓ | ✓ | ✓ | **3/3** | 5.9s | ~69 |  |
| big-pickle | opencode | Zen试用 | ✓ | ✓ | ✓ | **3/3** | 6.0s | ~66 | Zen试用配额 |
| nemotron-3.5-lightning-free | opencode | Zen试用 | ✓ | ✓ | ✓ | **3/3** | 7.1s | ~71 | Zen试用配额 |
| grok-4.7 | opencode-go | $15 | ✓ | ✓ | ✓ | **3/3** | 7.1s | ~48 |  |
| glm-5.3 | opencode-go | $15 | ✓ | ✓ | ✓ | **3/3** | 7.2s | ~48 |  |
| hy3 | opencode-go | $60 | ✓ | ✓ | ✓ | **3/3** | 7.6s | ~44 |  |
| deepseek-v4.1-flash | opencode-go | $100 | ✓ | ✓ | ✓ | **3/3** | 8.0s | ~40 | 订阅内最强全能 |
| iceman-contributor-free | opencode-go | ∞ 限时 | ✓ | ✓ | ✓ | **3/3** | 8.7s | ~36 | 当前默认 · 唯一无限免费 |
| glm-5.3-flash-free | opencode | Zen试用 | ✓ | ✓ | ✓ | **3/3** | 8.7s | ~35 | Zen试用配额 |
| step-5-preview | opencode-go | $15 | ✓ | ✓ | ✓ | **3/3** | 9.5s | ~37 |  |
| mimo-v2.6-pro | opencode-go | $15 | ✓ | ✓ | ✓ | **3/3** | 9.5s | ~45 |  |
| kimi-k3.1-pro | opencode-go | $15 | ✓ | ✓ | ✓ | **3/3** | 9.6s | ~32 |  |
| longcat-2.0 | opencode-go | $60 | ✓ | ✓ | ✓ | **3/3** | 9.7s | ~4 |  |
| kimi-k2.7-code | opencode-go | $60 | ✓ | ✓ | ✓ | **3/3** | 10.1s | ~28 |  |
| gemini-4-argon | opencode-go | $30 | ✓ | ✓ | ✓ | **3/3** | 10.2s | ~41 |  |
| qwen3.8-flash | opencode-go | $30 | ✓ | ✓ | ✓ | **3/3** | 10.8s | ~58 |  |
| mimo-v2.6-flash | opencode-go | $60 | ✓ | ✓ | ✓ | **3/3** | 10.9s | ~37 |  |
| kimi-k3 | opencode-go | $15 | ✓ | ✓ | ✓ | **3/3** | 12.1s | ~23 |  |
| qwen3.8-max | opencode-go | $15 | ✓ | ✓ | ✓ | **3/3** | 13.4s | ~32 |  |
| claude-haiku-5-5 | opencode-go | $15 | ✓ | ✓ | ✓ | **3/3** | 14.6s | ~17 |  |
| deepseek-v4-pro | opencode-go | $15 | ✓ | ✓ | ✓ | **3/3** | 17.4s | ~14 |  |
| qwen3.7-plus | opencode-go | $60 | ✓ | ✓ | ✓ | **3/3** | 20.1s | ~19 |  |
| hy4-preview | opencode-go | $30 | ✓ | ✓ | ✓ | **3/3** | 22.3s | ~10 |  |
| flint-40b-free | opencode | Zen试用 | ✓ | ✓ | ✓ | **3/3** | 23.2s | ~15 | Zen试用配额 |
| nemotron-3.5-super-vl-free | opencode | Zen试用 | ✓ | ✓ | ✓ | **3/3** | 43.0s | ~7 | Zen试用配额 |
| minimax-m3.1-flash | opencode-go | $20 | ✗ | ✓ | ✓ | **2/3** | 4.6s | ~126 |  |
| mimo-v2.6-flash-free | opencode | Zen试用 | ✗ | ✗ | ✓ | **1/3** | 18.3s | ~19 | Zen试用配额 |
| gpt-6-luna | opencode-go | $15(区域锁) | — | — | — | ERR | — | — | Country, region, or territory not supported |
| gpt-5.6-luna | opencode-go | $15(区域锁) | — | — | — | ERR | — | — | Country, region, or territory not supported |
| mimo-v2.5 | opencode-go | $60 | — | — | — | ERR | — | — | Model mimo-v2.5 has been deprecated |
| mimo-v2.5-pro | opencode-go | $15 | — | — | — | ERR | — | — | Model mimo-v2.5-pro has been deprecated |
| muse-spark-1.3-contributor | opencode-go | $60(区域锁) | — | — | — | ERR | — | — | This model is not available in your country |
| muse-spark-1.2-contributor | opencode-go | $60(区域锁) | — | — | — | ERR | — | — | This model is not available in your country |
| gpt-6-astra | relay | LAN relay | — | — | — | ERR | — | — | ECONNREFUSED（relay 离线） |

## 结论

- **日常默认**：`iceman-contributor-free` — 唯一无限免费（限时）+ 3/3 + 中速
- **主力升级**：`deepseek-v4.1-flash` — $100/月全场最大额度 + 3/3 + 快
- **高频 agent**：`minimax-m3` — 最快 + 3/3 + $60
- **硬骨头**：`glm-5.3` / `kimi-k3.1-pro` / `qwen3.8-max` / `gemini-4-argon`（全对，$15-30 小额度）
- **尝鲜**：Zen free 八件套；`mimo-v2.6-flash-free` 智力掉档、`nemotron-3.5-super-vl-free` 极慢
- **不可用**：gpt-luna×2、muse-spark×2、beam×2 区域锁；mimo-v2.5×2 已弃用；LAN relay 离线

原始数据：`results.json`；可视化报告：`report.html`（本地打开）。