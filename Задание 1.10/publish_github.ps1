# Скрипт публикации homework-04 на GitHub
# Запуск: powershell -ExecutionPolicy Bypass -File publish_github.ps1 -Token "ghp_ВАШ_ТОКЕН" -RepoName "data-platform-homework"

param(
    [Parameter(Mandatory=$true)]
    [string]$Token,
    
    [string]$RepoName = "data-platform-homework",
    [string]$Username = "valtureso788"
)

$ErrorActionPreference = "Stop"
$Headers = @{
    "Authorization" = "Bearer $Token"
    "Accept" = "application/vnd.github.v3+json"
    "X-GitHub-Api-Version" = "2022-11-28"
}

Write-Host "=== Создание репозитория $RepoName ===" -ForegroundColor Cyan

# 1. Проверяем, существует ли репозиторий
$repoUrl = "https://api.github.com/repos/$Username/$RepoName"
try {
    $existing = Invoke-RestMethod -Uri $repoUrl -Headers $Headers -Method GET
    Write-Host "Репозиторий уже существует: $($existing.html_url)" -ForegroundColor Yellow
} catch {
    # Создаём новый репозиторий
    $body = @{
        name = $RepoName
        description = "Домашние задания по курсу Data Platform"
        private = $false
        auto_init = $false
    } | ConvertTo-Json
    
    $repo = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Headers $Headers -Method POST -Body $body -ContentType "application/json"
    Write-Host "Репозиторий создан: $($repo.html_url)" -ForegroundColor Green
}

# 2. Устанавливаем remote и push
$repoDir = "C:\Users\Windows\Desktop\Задание 1.10"
Set-Location $repoDir

$remoteUrl = "https://${Username}:${Token}@github.com/${Username}/${RepoName}.git"

git remote remove origin 2>$null
git remote add origin $remoteUrl
Write-Host "Remote добавлен" -ForegroundColor Green

# Push main
git push -u origin main 2>&1 | ForEach-Object { Write-Host $_ }
Write-Host "Ветка main отправлена" -ForegroundColor Green

# Push hw-04
git push -u origin hw-04 2>&1 | ForEach-Object { Write-Host $_ }
Write-Host "Ветка hw-04 отправлена" -ForegroundColor Green

# 3. Создаём Pull Request
Write-Host "`n=== Создание Pull Request ===" -ForegroundColor Cyan
$prBody = @{
    title = "hw-04: план запроса и индексы MongoDB"
    head = "hw-04"
    base = "main"
    body = @"
## Домашнее задание № 4 — Plan запроса и индексы

Выполнен практикум «Онлайн-разбор запроса: explain и индексы».

### Содержимое lesson_04/

| Файл | Описание |
|---|---|
| README.md | Отчёт с анализом планов |
| plan-1.json | Q1 без индекса (COLLSCAN: 1200 docs) |
| plan-2.json | Q1 с ESR-индексом {service,level,ts,duration_ms} (оптимально: 33 docs) |
| plan-3a.json | Q1 {duration_ms,service,level,ts} (Range первый: 378 keys) |
| plan-3b.json | Q1 {service,level,duration_ms,ts} (E-R-S: 33 keys) |
| plan-4-bez.json | Q2 без индекса (COLLSCAN: 1200 docs) |
| plan-4.json | Q2 с {level,duration_ms} (оптимально: 10 docs) |

Практикум: https://maximbytecamp.github.io/mongodb_theory_makarov/praktiki/onlayn-razbor-zaprosa/
"@
} | ConvertTo-Json -Depth 10

try {
    $pr = Invoke-RestMethod -Uri "https://api.github.com/repos/$Username/$RepoName/pulls" -Headers $Headers -Method POST -Body $prBody -ContentType "application/json"
    Write-Host "`n✅ Pull Request создан!" -ForegroundColor Green
    Write-Host "URL: $($pr.html_url)" -ForegroundColor Cyan
} catch {
    Write-Host "⚠️ PR уже существует или ошибка: $_" -ForegroundColor Yellow
    # Получим список PR
    $prs = Invoke-RestMethod -Uri "https://api.github.com/repos/$Username/$RepoName/pulls" -Headers $Headers
    if ($prs.Count -gt 0) {
        Write-Host "Существующие PR:" -ForegroundColor Yellow
        $prs | ForEach-Object { Write-Host "  $($_.html_url)" }
    }
}

Write-Host "`n=== Готово! ===" -ForegroundColor Green
Write-Host "Репозиторий: https://github.com/$Username/$RepoName" -ForegroundColor Cyan
