# OVizLAB Skills — фоновое автообновление для рабочего Codex (Windows / LAB v0.1)

**Назначение:** автоматическая **периодическая проверка** публичного релиза OVizLAB и, после отдельного первоначального согласия владельца, **контролируемое обновление уже подтверждённых локальных Skills**. Это локальный Windows Scheduled Task, а не ChatGPT automation, облачный агент или сервис, действующий круглосуточно.

## Состояние и доступ

- **Частный основной репозиторий:** `lutiy-dev/GitHab-Skills` — приватный, продолжает содержать исходную разработку.
- **Планируемый открытый дистрибутив:** `lutiy-dev/OVizLAB-Skills`. Публичный репозиторий **пока не создан/не проверен**: на 2026-11-26 GitHub API ответил 404. До создания публичного канала обновления из другого аккаунта **SOURCE NOT ACCESSIBLE / BLOCKED**.
- В `OVizLAB-Skills` должен появиться доверенный `channel.json` в `main` и ZIP релиза с именем `ovizlab-agent-installer.zip`. Канал обновляется отдельно после проверки релиза; **не публиковать автоматически** из приватной ветки.
- Рабочий аккаунт Codex не должен получать GitHub-токены, личный ChatGPT Plugin или права на приватную разработку.

## Формат публичного канала

`https://raw.githubusercontent.com/lutiy-dev/OVizLAB-Skills/main/channel.json`:

```json
{
  "schema_version": 1,
  "repository": "lutiy-dev/OVizLAB-Skills",
  "sequence": 1,
  "source_commit": "<точный 40-значный SHA исходного утверждённого релиза>",
  "archive_url": "https://github.com/lutiy-dev/OVizLAB-Skills/releases/download/v1.0.0/ovizlab-agent-installer.zip",
  "archive_sha256": "<64 символа SHA-256 опубликованного ZIP>"
}
```

`sequence` — строго возрастающий номер публикации, а не номер версии Codex. Все поля должны быть фактическими. Не публиковать placeholders как рабочий канал.

**Trust model:** HTTPS к строго заданному GitHub repository, жёсткий URL-шаблон, SHA-256 ZIP, совпадение `bundle.json.source_commit`, контроль файлов внутри ZIP. SHA-256 в том же публичном GitHub-канале **не является криптографической независимой подписью владельца**: при компрометации публичного репозитория атакующий сможет подменить канал и архив. Для Production и обязательной неподделываемости потребуется независимая подпись и защищённый выпуск. Скачанный из нового релиза `install.py` **никогда не исполняется** updater: используется ранее одобренный локальный `agent_installer.py`.

## Первичное подключение (один раз, после ручного принятия baseline)

1. Получить из разрешённого источника подписанный или проверенный по независимому SHA полный архив и распаковать в **постоянную** пользовательскую директорию. Не запускать EXE из неизвестного источника, не отключать SmartScreen/Defender/ExecutionPolicy.
2. Установить Skills существующим `install.py` (сначала Dry Run, затем явное подтверждение и `--apply`). Убедиться, что все выбранные Skills точно соответствуют исходному `bundle.json`; пользовательские изменения и конфликты требуют отдельного решения.
3. Проверить Python 3.10+ / `py -3` и **сохранить в одной стабильной папке** `auto_update.py` и `agent_installer.py` из подтверждённого offline ZIP. Не заменять их автоматически последующими релизами.
4. После сверки `sequence` с подтверждённым публичным каналом и SHA установленного bundle дать **явное согласие на область фоновых обновлений** (только ранее установленные OVizLAB Codex Skills пользователя).
5. В папке доверенного распакованного архива запустить:

```powershell
py -3 .\auto_update.py enroll --bundle . --home "$env:USERPROFILE" --sequence 1
py -3 .\auto_update.py status
py -3 .\auto_update.py check
```

`enroll` записывает базовый state в `$env:LOCALAPPDATA\OVizLAB\auto-update\state.json` **только если все Skills из исходного ZIP точно совпали с существующими на диске**. Она **не устанавливает и не заменяет Skills** и **не создаёт scheduled task**. `sequence 1` — пример; использовать фактическое значение канала, не угадывать.

## Preview → включение ежедневного background task

В стабильной директории с `auto_update.py`:

```powershell
powershell -NoProfile -File .\ovizlab_auto_update_task.ps1 -Enable -UpdaterScript "$PWD\auto_update.py"
```

Предварительный просмотр не меняет Windows. После изучения реального `TaskName`, пути updater, `state.json`, Python executable, ежедневного времени **10:00 по локальному времени**, и scope, владелец подтверждает создание одного задания:

```powershell
powershell -NoProfile -File .\ovizlab_auto_update_task.ps1 -Enable -UpdaterScript "$PWD\auto_update.py" -Apply
```

По умолчанию Task Scheduler запускает обновление ежедневно, **когда пользователь вошёл в Windows**. Нет прав администратора, службы, глобальных hooks, изменения ACL/MCP/Codex settings, входа через другой GitHub аккаунт. Регистрация чужой одноимённой задачи запрещена. Если групповая политика, права или ExecutionPolicy блокируют создание: **STOP**, не обходить ограничения.

При каждом вызове `auto_update.py run`:

1. Прочитать и проверить `state.json`, channel URL, возрастающий номер релиза.
2. Если релиз не изменился → `UP_TO_DATE`, никакой записи в Skills.
3. Если релиз новый → до скачивания проверяется отсутствие локального drift во **всех** ранее подтверждённых Skills.
4. Скачать ZIP с максимальным размером, проверить SHA и manifest и безопасно распаковать в новую временную папку.
5. Если из набора прежних Skills что-либо удалено, или появился конфликт → **BLOCKED** без замены.
6. Обновить **только ранее подтверждённые Skills**, не устанавливать автоматически новые, с существующим `agent_installer.execute` и резервными копиями `.ovizlab-backups/.../receipt.json`.
7. После успешного apply атомарно обновить локальный state. Новый Skill требует отдельного согласия. Если state не обновился после выполненной транзакции, сохранённый receipt — точка восстановления; **не запускать повторно вслепую**.

Это **реальное фоновое обновление после однократного согласия** на ограниченный набор файлов, а не самостоятельное разрешение менять систему. Не создавать silent install для неподтверждённых Skills. Agent discovery в работающем Codex не обновится до нового сеанса; `FILES VERIFIED` ≠ `DISCOVERY VERIFIED`.

## Остановка и откат

**Остановить фоновые проверки без удаления Skills:**

```powershell
powershell -NoProfile -File .\ovizlab_auto_update_task.ps1 -Disable
powershell -NoProfile -File .\ovizlab_auto_update_task.ps1 -Disable -Apply
```

После отключения task не запускается. State и архивы можно оставить для диагностики; автоматически не удалять. **Чтобы откатить изменённые Skills**, после проверки точного `receipt.json` и текущих файлов использовать штатный installer:

```powershell
py -3 install.py --rollback-receipt "<проверенный receipt.json>" --apply
```

После rollback старый `state.json` может больше не соответствовать установленным файлам; его нельзя исправлять вручную наугад. Пересогласовать baseline / повторно enrollment после полной проверки.

## Контроль качества

- `GENERATED`: исходники updater и scheduler подготовлены.
- `VALIDATED`: синтетические unit tests успешны на точном CI SHA.
- `WINDOWS SCHEDULER TESTED`: только после реального изолированного Windows теста регистрации/запуска/удаления task.
- `PUBLIC RELEASE AVAILABLE`: только когда публичный GitHub Release и канал реально доступны без авторизации.
- `WORK ACCOUNT FIELD PASS`: фактическая проверка обновления и read-back из Codex под рабочим аккаунтом.
- `PRODUCTION STANDARD`: отдельный security review, внешний trust/signing и подтверждение владельца.

В этой ветке **нет автоматической публикации, регистрации Windows Task Scheduler, изменения установленного OVizLAB Plugin или рабочего компьютера**.
