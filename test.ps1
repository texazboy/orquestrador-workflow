# Equivalente Windows do "make test".
# Roda os 3 niveis, compara a saida com o gabarito (comparacao canonica, com as
# chaves ordenadas) e por fim roda os testes de unidade.
# Uso:  .\test.ps1
Set-Location -Path $PSScriptRoot

$py = "python"
$niveis = @("basico", "avancado", "estresse")
$ok = $true

Write-Host "== Comparando saida x gabarito =="
foreach ($n in $niveis) {
    $tmp = Join-Path $env:TEMP "saida_$n.json"
    # 2>&1 | Out-Null descarta o resumo que o programa imprime no stderr
    & $py -m src.main --input "data/input_$n.json" --output $tmp 2>&1 | Out-Null
    $a = & $py -c "import json;print(json.dumps(json.load(open(r'$tmp',encoding='utf-8')),sort_keys=True,ensure_ascii=False))"
    $b = & $py -c "import json;print(json.dumps(json.load(open(r'data/output_esperado_$n.json',encoding='utf-8')),sort_keys=True,ensure_ascii=False))"
    if ($a -eq $b) {
        Write-Host ("[OK]    {0}: saida bate com o gabarito" -f $n) -ForegroundColor Green
    } else {
        Write-Host ("[FALHA] {0}: saida DIVERGE do gabarito" -f $n) -ForegroundColor Red
        $ok = $false
    }
    Remove-Item $tmp -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "== Testes de unidade =="
& $py -m unittest tests.test_casos
if ($LASTEXITCODE -ne 0) { $ok = $false }

Write-Host ""
if ($ok) {
    Write-Host "==> Todos os niveis passaram." -ForegroundColor Green
    exit 0
} else {
    Write-Host "==> Houve divergencia." -ForegroundColor Red
    exit 1
}
