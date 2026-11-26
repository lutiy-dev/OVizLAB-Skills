# OVizLAB Skills — каталог для AI-агента

> Подтверждённый inventory: 28 Skills из `lutiy-dev/GitHab-Skills/main` на 2026-11-26. Краткое назначение — пересказ frontmatter; source of truth — актуальный `skills/<slug>/SKILL.md`.

| Skill | Для каких задач |
| --- | --- |
| `3dsmax-maxscript` | MAXScript/pymxs с проверкой безопасности 3ds Max-сцены |
| `android-release-verifier` | Релиз Android APK: Gradle, CI, подпись, обновления, реальные устройства |
| `archviz-ai-finishing` | Маскированная AI-доработка Corona рендеров с Geometry QC |
| `archviz-animation-director` | Архитектурная камера и сценарий анимационных шотов |
| `archviz-atmosphere-lighting` | Свет, сезон, погода и атмосфера без изменения архитектуры |
| `archviz-geometry-guardian` | Сохранение исходной геометрии и пропорций при визуализации и AI-редактировании |
| `archviz-material-lookdev` | Физически правдоподобные материалы и QA 3ds Max/Corona |
| `archviz-portfolio-director` | Планирование и отбор работ коммерческого портфолио |
| `archviz-shot-director` | Композиция и storytelling фотореалистичных экстерьеров |
| `archviz-vfx-compositing` | Контролируемый compositing, VFX, отражения и эффекты |
| `archviz-video-editing` | Монтаж showreel/фильмов с проверкой delivery и прав |
| `browser-document-operator` | Работа с браузером, документами и формами с проверяемым результатом |
| `codex-usage-guardian` | Сокращение затрат Codex при сохранении проверок |
| `comfyui-workflow-builder` | Импортируемый ComfyUI JSON, pinned-модели/ноды, QC |
| `creative-image-direction` | Art direction изображений, промпты, референсы и critique |
| `decision-interview` | Выявление неопределённостей и выбор проверяемого решения |
| `h3-prompt-writing` | Промпты MiniMax H3 для видео и мультимодальных референсов |
| `pages-pwa-verifier` | GitHub/Cloudflare Pages, PWA и реальный браузерный QA |
| `portfolio-delivery-qc` | Финальные изображения/анимации, метаданные, экспорты |
| `pr-ci-verifier` | Проверка PR и CI по точному SHA |
| `regression-guardian` | Regression, browser и functional QA |
| `repository-auditor` | Read-only аудит репозитория и зависимостей |
| `safe-implementer` | Контролируемые изменения, scope, rollback и safety gates |
| `skill-discovery` | LOCAL FIRST поиск Skills с проверкой источника |
| `skill-maintainer` | Аудит сторонних Skills: права, безопасность, лицензия, дубли |
| `web-frontend-builder` | Доступные responsive web-интерфейсы и браузерные проверки |
| `web3d-gltf-pipeline` | 3ds Max → glTF/GLB → интерактивный web-3D |
| `windows-system-diagnostics` | Диагностика Windows/PowerShell и Codex sandbox |

## Как выбирать

1. Сначала задача пользователя, потом минимальный релевантный Skill.
2. Читать `SKILL.md` и нужные `references/`, сверять действительную версию, инструмент и разрешения.
3. `FILES VERIFIED` не означает, что Codex его прочитал. `DISCOVERY VERIFIED` требует реального host read.
4. Запрещены несогласованная перезапись, загрузка исполняемых файлов из непроверенных источников, изменение глобальных настроек и автоприменение.

## Cross-account доступ

GitHub API на момент создания документа показывает `private=true`. Другая учётная запись Codex/GitHub без соответствующего доступа не сможет получить репозиторий по URL. Использовать явно разрешённый доступ GitHub, доверенный offline archive либо отдельно одобренный публичный дистрибутив. Никаких токенов в чате или файлах.

[Пошаговая инструкция установки и обновления для агента](AGENT_INSTALL_AND_UPDATE.md).
