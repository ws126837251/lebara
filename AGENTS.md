# Lebara 使用指南网站维护规则

## 项目概览

- 本仓库是由 Gmeek 生成并通过 GitHub Pages 发布的静态博客。
- 生产站点：`https://tutorials.wufeng.de/lebara/`
- 主要配置：`config.json`
- 自动化工作流：`.github/workflows/Gmeek.yml`
- 文章的原始内容来自本仓库的 GitHub Issues。
- 工作流会在 Issue 新建或编辑、手动触发以及每日定时任务运行时重新生成并发布网站。

## 文件职责

- `config.json`：站点标题、说明、主题注入脚本和 Gmeek 版本等源配置。
- `article-order.json`：首页自定义置顶文章及其精确显示顺序，不限制数量。
- `.github/workflows/Gmeek.yml`：生成、定制、验证和部署流程。
- `scripts/customize_homepage.py`：按自定义顺序处理并校验生成后的首页。
- `tests/test_customize_homepage.py`：自定义顺序与配置校验测试。
- `docs/`：工作流生成的发布文件，不应直接手工维护。
- `backup/`：工作流生成的文章备份，不应作为文章的主要编辑入口。
- `blogBase.json`：Gmeek 生成的数据文件，不应直接编辑。

## 修改原则

- 修改文章内容时，优先编辑对应的 GitHub Issue，不要直接修改 `docs/post/*.html` 或 `backup/*.md`。
- 修改站点样式或功能时，先判断应修改 `config.json` 的注入内容，还是修改 `.github/workflows/Gmeek.yml` 的生成后处理。
- 不要为了修复生成结果而直接编辑生成文件；应修复配置或生成流程，再让工作流重新生成。
- 保留现有中文内容和 UTF-8 编码，避免使用会造成中文乱码的默认编码写入方式。
- 对工作流做最小范围修改，不随意扩大 GitHub Actions 权限，不引入未经说明的第三方 Action。
- `GMEEK_VERSION` 当前为 `main`。除非用户明确要求，不要擅自切换版本或固定到其他提交。

## 维护备份规则

- 每次人工修改源文件之前，必须先在 `maintenance-backups/` 下创建独立快照。
- 快照目录采用 `YYYY-MM-DD_序号_before-任务名` 命名，并保留原文件名和相对路径信息。
- 每个快照必须包含 `manifest.md`，记录创建时间、任务名称、原始文件和恢复方法。
- `backup/` 是 Gmeek 自动生成的文章备份目录，不得用于保存人工维护快照。
- `docs/`、`backup/` 和 `blogBase.json` 等生成结果不单独备份；应备份真正修改的源配置、工作流或文章 Issue 内容。
- 人工维护快照只保留最新 3 个版本；创建新快照后若总数超过 3 个，按目录名排序删除最早的版本，直至只剩 3 个。
- 除按上述滚动规则清理最早版本外，不覆盖、改写或删除仍在保留期内的快照。

## 验证要求

- 修改 `config.json` 后，必须验证它是合法 JSON。
- 修改内嵌 HTML、CSS 或 JavaScript 后，检查 JSON 转义、浏览器控制台错误和移动端显示。
- 修改工作流后，检查 YAML 语法、触发条件、权限、生成目录以及 Pages 部署步骤。
- 发布前优先查看 GitHub Actions 构建结果，并检查首页、文章页、标签页和 RSS。
- UI 修改至少检查桌面端和移动端。

## 发布与安全

- 未经用户明确确认，不执行 `git push`、不触发生产部署、不修改域名或 GitHub Pages 设置。
- 未经用户明确确认，不关闭或删除工作流、Issue、文章和生成文件。
- 不把令牌、Cookie、私钥或其他秘密写入仓库。
- 不在日志中输出敏感环境变量。
- 若需要 GitHub 写操作，优先使用用户授权的 GitHub 连接；执行前明确说明会修改什么。
