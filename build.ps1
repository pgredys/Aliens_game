$content = Get-Content high_score.log -Raw
Clear-Content high_score.log

pyinstaller alien_invasion.spec

Add-Content high_score.log $content

Remove-Item -LiteralPath "release" -Force -Recurse
New-Item -Name "release" -ItemType "directory"

Copy-Item -Path "assets/audio" -Destination "release/assets/audio" -Recurse
Copy-Item -Path "assets/fonts" -Destination "release/assets/fonts" -Recurse
Copy-Item -Path "assets/imgs" -Destination "release/assets/imgs" -Recurse
Move-Item -Path "build" -Destination "release"
Move-Item -Path "dist" -Destination "release"

$compress = @{
Path= "release/*"
CompressionLevel = "Fastest"
DestinationPath = "release/Alien_Invasion_X_X.zip"
}
Compress-Archive @compress