$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$powerpoint = $null
try {
    $powerpoint = New-Object -ComObject PowerPoint.Application
    $files = Get-ChildItem -Path (Join-Path $root 'Nguoi_*\output\Nguoi_*_slides*.pptx')
    foreach ($file in $files) {
        $previewName = if ($file.BaseName -like '*_5min') { 'preview_5min' } else { 'preview' }
        $preview = Join-Path $file.Directory.FullName $previewName
        New-Item -ItemType Directory -Path $preview -Force | Out-Null
        $presentation = $null
        try {
            $presentation = $powerpoint.Presentations.Open($file.FullName, -1, 0, 0)
            foreach ($slide in $presentation.Slides) {
                $target = Join-Path $preview ('slide_{0:D2}.png' -f $slide.SlideIndex)
                $slide.Export($target, 'PNG', 1920, 1080)
                [void][Runtime.InteropServices.Marshal]::ReleaseComObject($slide)
            }
            Write-Output "$($file.Name): $($presentation.Slides.Count) previews -> $preview"
        } finally {
            if ($null -ne $presentation) {
                $presentation.Close()
                [void][Runtime.InteropServices.Marshal]::ReleaseComObject($presentation)
            }
        }
    }
} finally {
    if ($null -ne $powerpoint) {
        $powerpoint.Quit()
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($powerpoint)
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
