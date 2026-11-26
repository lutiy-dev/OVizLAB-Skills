# OVizLAB — установка и обновление Skills из другого аккаунта Codex

**Для AI coding agents (Codex / Claude Code), а также владельца компьютера.** Это инструкции, а не разрешение на файловые изменения. Source of truth: `lutiy-dev/GitHab-Skills` → `skills/<slug>/SKILL.md`. [Каталог 28 Skills](OVIZLAB_AGENT_SKILLS_CATALOG.md).

## 0. Принцип и ограничение доступа

На 2026-11-26 репозиторий `lutiy-dev/GitHab-Skills` имеет статус **PRIVATE** по GitHub API. Личный ChatGPT OVizLAB Plugin 0.3.2 **не переносится** в другой аккаунт Codex и сам по себе не предоставляет ему доступ к GitHub.

Для самостоятельной загрузки обновлений агенту необходим один из **законных, разрешённых** источников:
1. GitHub аккаунт/connector с доступом к приватному репозиторию, предоставленным владельцем через обычный GitHub permission flow (не передавать токены в чат);
2. заранее скачанный владельцем **проверенный offline ZIP** `ovizlab-agent-installer.zip`, доступный на локальном ПК;
3. отдельный публичный дистрибутив / mirror только после явно одобренной владельцем публикации и проверки прав/секретов.

Без любого из этих источников: **STOP / SOURCE NOT ACCESSIBLE**. Не обходить авторизацию, не использовать случайные fork, raw/ZIP ссылки или невалидированные third-party packages.

## 1. Агент: READ-ONLY preflight

1. Установить фактическую среду (Codex/Claude, Windows, CLI/Desktop/cloud), полномочия, user/project scope и каталог пользователя. На рабочем ПК чужого аккаунта **не угадывать** пути.
2. Определить существующий каталог Skills, например для Codex user scope `$env:USERPROFILE\.agents\skills`. Каталог `$env:USERPROFILE\.codex\skills` может хранить служебные Skills и не является безусловным destination.
3. Провести инвентаризацию существующих Skills, сравнить с актуальным [каталогом](OVIZLAB_AGENT_SKILLS_CATALOG.md) и проверить локальные изменения, symlinks, права/конфликты.
4. Узнать версию доверенного источника: полный Git HEAD SHA или `bundle.json.source_commit`. Сверить с ранее установленными file hashes; **наличие папки не доказывает актуальную версию**.
5. Если источник недоступен, показать status и необходимые разрешения. **Никаких изменений.**

## 2. Получение нового trusted bundle

**Рекомендуемый вариант:** владелец или авторизованный агент получает конкретный официальный archive из подтверждённого GitHub Actions run. Артефакты GitHub Actions приватного репозитория обычно требуют разрешённый GitHub доступ; не считать их публично доступными.

**Альтернатива для агента с разрешённым GitHub read access:** построить пакет из полностью проверенного checkout, не выполняя scripts из непроверенного remote:

```powershell
# Выполнять только в уже проверенном и авторизованном checkout GitHab-Skills
git status --short
git rev-parse HEAD
py -3 tools/build_agent_installer.py --source-sha (git rev-parse HEAD) --output dist/ovizlab-agent-installer.zip
Get-FileHash dist/ovizlab-agent-installer.zip -Algorithm SHA256
```

**STOP** при dirty checkout, unexpected base, ошибке канонических mirrors, отсутствии Python, невалидном SHA или отсутствии разрешённого GitHub доступа. Этот путь **не обещает** автоматически скачать обновление с private GitHub под другим аккаунтом.

Если пакет уже получен, агент должен распаковать его в новую **проверенную временную директорию**, не смешивая с текущими установленными Skills, и проверить происхождение/expected SHA и `bundle.json`. Не отключать PowerShell ExecutionPolicy/Defender/SmartScreen и не запускать unsigned EXE в автоматическом режиме.

## 3. Dry Run — ОБЯЗАТЕЛЕН

Архив содержит `install.py` (Python 3.10+ stdlib) и `bundle.json`. В каталоге **доверенного распакованного архива**:

```powershell
py -3 install.py --agent codex
# При необходимости ещё и Claude: py -3 install.py --agent codex --agent claude
```

Без `--apply` никаких Skills не устанавливается. Инсталлятор должен показать `INSTALL`, `SKIP`, `BACKUP+REPLACE`, полный source SHA и путь назначения.

Агент должен сверить точный список заменяемых файлов, сохранность пользовательских Skills и источник. Если пользователь модифицировал Skills, не перезаписывать молча — обсудить конфликт. Не менять `AGENTS.md`, `CLAUDE.md`, hooks, MCP settings, модель, права, конфигурацию ComfyUI или 3ds Max.

## 4. Controlled update

Только после **явного разрешения на конкретный план изменений**:

```powershell
py -3 install.py --agent codex --apply
```

Повторные установки одинаковых Skills — `SKIP`. При замене инсталлятор создаёт резервную копию и `receipt.json` в `.ovizlab-backups`. Сохранять `receipt.json` и исходный trusted archive. Не запускать повторно после частичного FAIL до диагностики.

**Фоновое автообновление (отдельный LAB-модуль):** базовый `install.py` остаётся ручным. При наличии доступного публичного канала владелец может явно включить `auto_update.py` и Windows Scheduled Task по [инструкции](OVIZLAB_BACKGROUND_UPDATES.md). После enrollment система автоматически обновляет только заранее подтверждённые, неизменённые Skills, сохраняет receipts, блокирует downgrade и неизвестные новые Skills. Без enrollment и отдельного включения task нет фоновых проверок/записей. Публичный канал пока не опубликован.

## 5. Verify и rollback

1. Повторно проверить контрольные суммы установленных файлов по `bundle.json`, необходимый reference и наличие `Image Edit Contract (LAB v0.6)` в `archviz-geometry-guardian/SKILL.md`.
2. В **новом Codex-сеансе** попросить агента прочитать точный установленный `SKILL.md` и подтвердить source path. Только это может дать `DISCOVERY VERIFIED`; файл на диске = `FILES VERIFIED`.
3. Реальное исполнение инструмента и независимая проверка результата — отдельный `RUNTIME TESTED`. Реальная защита Guard на уровне host — самостоятельный security gate.
4. Для возврата к предыдущему состоянию после согласия пользователя:

```powershell
py -3 install.py --rollback-receipt "<проверенный путь к receipt.json>" --apply
```

При изменённом после установки Skill инсталлятор блокирует откат вместо потери пользовательских данных.

## 6. Reusable prompt для другого аккаунта Codex

> Ты работаешь на другом аккаунте. Найди локальные OVizLAB Skills и безопасно проверь наличие обновлений из разрешённого источника `lutiy-dev/GitHab-Skills`. Ознакомься с `README_FOR_AGENTS.md`, `OVIZLAB_AGENT_SKILLS_CATALOG.md` и этим документом, если они доступны. Если repository private и прав GitHub нет, используй только предоставленный мной проверенный offline package, не обходи авторизацию. Сначала READ-ONLY inventory и source SHA, затем dry-run. Выдай PLAN с INSTALL/SKIP/BACKUP+REPLACE, рисками и rollback. Без моего разрешения ничего не устанавливай и не перезаписывай. После одобрения выполни один controlled update и отдельно докажи FILES VERIFIED и DISCOVERY VERIFIED. Не считай наличие ChatGPT Plugin доказательством доступа Codex.

**STOP:** private source inaccessible; no trusted artifact; unexpected repo/SHA; invalid file inventory; unapproved overwrite; altered user files; missing rollback; platform/security restrictions.

**Статусы:** GENERATED → VALIDATED → FILES VERIFIED → DISCOVERY VERIFIED → RUNTIME TESTED; не перескакивать через этапы.
