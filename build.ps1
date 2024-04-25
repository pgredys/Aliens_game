$content = Get-Content high_score.log -Raw
Clear-Content high_score.log
pyinstaller alien_invasion.spec
Add-Content high_score.log $content