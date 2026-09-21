# mattpocock-skills

Matt Pocock 上游技能集的非官方个人 fork，打包成原生 Claude Code 插件分发。本仓库同时是插件产物本身与它的编写台：分发读的是提交进 `plugin/` 的技能正文，而 `skills` 白名单决定哪些技能真的会被加载。编写台的那一半——模板、共享正文、脚本——一律待在 plugin root 之外，不会被复制到用户机器上。

## Language

### 打包与分发

**Skill**:
本插件分发的内容单位：一个含 `SKILL.md` 的目录，其 frontmatter 的 `description` 决定 agent 何时自己触发它。人按名调用时它表现为斜杠命令，但它不是命令。
_Avoid_: command、prompt、agent、tool

**Plugin**:
分发单位：一个可被 Claude Code 安装的包，装完后其技能以带命名空间的命令出现。本仓库自己就是它的插件源。
_Avoid_: package、extension、skill pack

**Marketplace**:
让一个 git 仓库成为可安装来源的清单。本仓库是只含自己这一个插件的 marketplace，所以 `marketplace add` 是 `install` 的前置步骤而非可选步骤。
_Avoid_: registry、index、app store

**Manifest**:
`plugin/.claude-plugin/plugin.json`：插件的名字、版本与 `skills` 白名单。它是本仓库唯一跟随上游发版本节奏的文件。
_Avoid_: config、plugin file、metadata

**Plugin root**:
分发时被整体复制走的那个目录：本仓库的 `plugin/`。插件缓存里的内容就是它的递归副本，所以任何不该出现在用户机器上的东西都必须待在它之外。
_Avoid_: plugin dir、dist dir、package root

**Whitelist**:
manifest 里的 `skills` 数组，按目录路径列出要加载的技能。它是加载与否的唯一依据：目录存在但不入列就等于不存在。
_Avoid_: skill list、include list、enabled list

**Enabled skill**:
目录在 `plugin/skills/<category>/<name>/` 且路径在白名单里的技能：会被加载，调用名是 `/mattpocock-skills:<name>`。
_Avoid_: active skill、installed skill、live skill

**Folded skill**:
上游有、本仓库不作为独立条目发布，而是把正文内联进消费方技能的那种：`grilling` 折进 `grill-me`、`grill-with-docs`，以及内部同样跑这份协议的 `triage`、`wayfinder`、`improve-codebase-architecture`；`domain-modeling` 折进 `grill-with-docs`。正文的唯一副本在 `dev/source/<unit>/`，由 template 渲染进消费方目录，所以它没有自己的命令，只会作为消费方技能的一部分出现。
_Avoid_: merged skill、inlined skill、delisted skill

**Namespace**:
已安装插件的调用前缀 `/mattpocock-skills:`。插件技能总是带命名空间，没有裸名调用。
_Avoid_: prefix、scope

**Upstream**:
`mattpocock/skills`，技能正文的事实来源。本仓库不追它的发布节奏。
_Avoid_: origin、base repo、source repo

**Fork**:
本仓库自身：upstream 的非官方个人分支，收窄到实际在用的技能集，并把两个上游技能折叠进消费方而不单独分发（grilling、domain-modeling）。
_Avoid_: clone、downstream、derivative

**Divergence**:
fork 与 upstream 之间刻意保留的差异；不写明就会被读成失同步。本仓库有四处：领域文档约定改名为 `GLOSSARY.md`、互相打架的约定之间做了调和、grilling 与 domain-modeling 被折叠进消费方、setup 技能改名为 mattpocock-skills-setup。
_Avoid_: diff、delta、customization

**Re-sync**:
把本仓库 `plugin/skills/` 按相同路径与 upstream 做 diff，再搬入变化的那一步。manifest 只在 upstream 发版本时跟一次。
_Avoid_: merge、update、pull、upgrade

### 编写与渲染

**Source unit**（`dev/source/<unit>/`）:
被多个技能共享的一段正文的唯一副本，一个共享单元一个子目录。它在 plugin root 之外：既不在任何白名单路径下，也绝不能被列入白名单。
_Avoid_: partial、fragment、shared folder、include dir

**Template**（`dev/templates/<plugin 相对路径>.tmpl`）:
手写的那一侧：一份需要被引入共享正文的文件的源。它放在 `dev/templates/` 下并镜像 plugin 树，与其渲染产物分居两处。
_Avoid_: source file、input file、blueprint

**Target**（`plugin/<plugin 相对路径>`）:
template 渲染出的那一侧，提交进仓库，落在 plugin root 内。插件分发直接读它，加载路径上没有构建步骤。
_Avoid_: generated file、build output、artifact、dist

**Include placeholder**（`{{include:<相对仓库根的路径>}}`）:
template 里独占一整行的那一行，渲染时被目标文件的完整内容替换。逐字且只下一层：被引入文件自己再出现 placeholder 也不会二次渲染。
_Avoid_: directive、macro、import、tag

**Render**:
把每个 template 变成其镜像 target 的那一步：字节一致则不动，不同则原子替换，可重复执行而不产生噪音。
_Avoid_: build、compile、bundle

**Shim**:
消费方技能目录里只含一个 include placeholder 的一行式 template。存在的理由是把共享单元的文件在消费目录内也渲染出一份，好让相对同级的链接（`[DEEPENING.md](DEEPENING.md)`）在插件实际读的那个目录里解析得到。它是 template，所以在 `dev/templates/` 下对应消费方技能的镜像位置。
_Avoid_: stub、proxy file、re-export、symlink

### 每仓库配置

**Setup**:
`mattpocock-skills-setup` 这项每仓库跑一次的配置动作：定下 issue tracker、triage 标签词表、领域文档落位这三件事。它的产物是 `docs/agents/` 下的三份文件，加 `AGENTS.md` / `CLAUDE.md` 里的一个块。
_Avoid_: install、init、bootstrap、onboarding

**Issue tracker**:
本仓库追踪 issue 的地方，由 setup 选定并记在 `docs/agents/issue-tracker.md`。`to-spec`、`to-tickets`、`code-review`、`triage` 都先读它，再决定该调 `gh` 还是写 markdown 文件。
_Avoid_: backlog、board、ticketing system

**Feature directory**（`.scratch/<feature-slug>/`）:
本仓库 local-markdown tracker 下一个 feature 的家：`spec.md` 加 `issues/<NN>-<slug>.md`，一个 ticket 一个文件、按依赖顺序从 `01` 编号。
_Avoid_: epic folder、work folder、scratch dir

**Triage label vocabulary**:
规范 triage 角色到 tracker 实际标签字符串的映射，记在 `docs/agents/triage-labels.md`。角色共七个：五个状态角色加两个分类角色。
_Avoid_: label scheme、taxonomy、status set

**Domain docs**:
`GLOSSARY.md` 与 `docs/adr/` 这对领域文档的落位及读取规则，记在 `docs/agents/domain.md`。技能写出的东西（issue 标题、测试名、重构提案、假设）都用它的词汇。
_Avoid_: domain documentation、docs layout、knowledge base

**Context**（single- vs multi-context）:
领域词汇的边界。single-context 是仓库根一份 `GLOSSARY.md`；根上出现 `GLOSSARY-MAP.md` 就是 multi-context，每个 context 各有一份。本仓库是 single-context。
_Avoid_: bounded context、module、scope、namespace
