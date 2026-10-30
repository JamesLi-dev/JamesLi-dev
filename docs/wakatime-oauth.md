# WakaTime 个人主页同步认证

WakaTime 邮件通知：从 2026-11-01 起，API key 仅供编辑器插件上传活动使用。
本仓库读取统计数据，需要改用个人 OAuth token，无需发布 OAuth 应用。

1. 登录 https://wakatime.com/oauth 获取个人 OAuth token，确保允许读取统计数据（`read_stats`）。
2. 在运行本工作流的 GitHub 仓库中打开 **Settings → Secrets and variables → Actions**，新增或更新名为 `WAKATIME_AUTH_TOKEN` 的 repository secret，值为该 token。
3. 将本次代码更新合并到 `master`；工作流引用的是 `JamesLi-dev/JamesLi-dev@master`，只修改本地文件不会改变线上同步。
4. 在 Actions 中手动运行 **Waka Readme**，检查执行结果和个人主页统计。

不要将 token 写进代码或 README。编辑器插件继续使用原 API key。

`main.py` 优先读取 `INPUT_WAKATIME_AUTH_TOKEN`，通过 `Authorization: Bearer ...` 发送。
`WAKATIME_API_KEY` 输入保留给 Wakapi/Hakatime 等兼容后端；本仓库工作流已改用新 secret。
缺少凭据或收到 401/403 时任务会失败，不覆盖现有 README。

当前 Docker Action 只运行 `main.py`，旧的 `moreMain.py` 不在此工作流执行链路中。

参考：[WakaTime 官方认证文档](https://wakatime.com/developers#authentication)。
