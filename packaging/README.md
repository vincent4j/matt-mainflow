# WorkBuddy 用户级离线套装

解压 `matt-mainflow-global-<版本>.zip`，在解压目录用 Python 3 运行一次安装命令。

```sh
python3 install.py
```

安装目录为 `~/.workbuddy/skills/`。已有同名但内容不同的 Skill 时，脚本会在写入前停止并显示路径。在 WorkBuddy 新建会话后，可直接选择 `/matt-mainflow`、`/to-spec`、`/tdd` 等入口。直接调用上游入口时使用原版行为，项目级配置按上游指引进行。

维护者在源码仓库根目录运行 `python3 packaging/build.py --global-suite` 即可生成套装。版本来自项目清单，ZIP 保存在本地 `dist/`。WorkBuddy 技能库的单技能导入使用 `matt-mainflow-offline-<版本>.zip`。
