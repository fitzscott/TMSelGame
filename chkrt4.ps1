for ($i = 0; $i -lt 5; $i++) {
    $disp = ""
    for ($inc = 0; $inc -lt 4; $inc++) {
    if ($inc -eq 0) {
        $sep = ""
    }
    else {
        $sep = ","
    }
    $nxt = $i + $inc * 5
    $disp += $sep + $nxt.ToString()
    }
    $sttm = get-date -Format "yyyy-MM-dd HH:mm:ss"
    python genTMgameopts.py ${disp} 1 | Select-Object -Last 3
    $entm = get-date -Format "yyyy-MM-dd HH:mm:ss"; Write-Output "set ${disp} ran ${sttm} - ${entm}"
}