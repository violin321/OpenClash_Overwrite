# IPv6 / noIPv6 版本说明

本 fork 在保留上游更新的基础上，额外提供了 **旁路由 IPv6 版** 覆写文件，适合希望旁路由场景开启 IPv6 代理的用户。

## 旁路由版本对照

### noIPv6 / 上游默认旁路由版本
- Smart-LGBM：`Overwrite/Overwrite-smart-bypass-LGBM.conf`
- Smart（默认模型 + 数据收集）：`Overwrite/Overwrite-smart-bypass.conf`

特点：
- 默认关闭 IPv6
- 更保守，适合先保证 IPv4 代理稳定的旁路由场景

---

### IPv6 / 本 fork 自动生成版本
- Smart-LGBM：`Overwrite/Overwrite-smart-bypass-LGBM-ipv6.conf`
- Smart（默认模型 + 数据收集）：`Overwrite/Overwrite-smart-bypass-ipv6.conf`

额外固定开启：
- `IPV6_ENABLE = 1`
- `IPV6_DNS = 1`
- `IPV6_MODE = 0`
- `ENABLE_V6_UDP_PROXY = 1`
- `CHINA_IP6_ROUTE = 1`

并将 `DOWNLOAD_FILE` 指向本 fork 的 `Yaml/Overwrite-Clash-Bypass.yaml`，便于自动同步上游后继续保留 IPv6 patch。

---

## 推荐选择

### 选 noIPv6 版，如果你：
- 旁路由 IPv6 环境不稳定
- 设备常常 IPv6 直连绕过代理
- 先只想稳定使用 IPv4 代理

### 选 IPv6 版，如果你：
- 已确认路由器 / 上游 / 节点都支持 IPv6
- 希望旁路由同时接管 IPv6 代理
- 能接受自己观察几天稳定性

---

## 自动同步说明

GitHub Actions 工作流：
- `.github/workflows/sync-upstream-ipv6.yml`

行为：
1. 同步上游 `Giveupmoon/OpenClash_Overwrite`
2. 重新生成两个旁路由 IPv6 版文件
3. 有变化则自动提交
