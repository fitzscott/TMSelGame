for ($i = 0; $i -lt 3; $i++) {
    $disp = ""
    for ($inc = 0; $inc -lt 7; $inc++) {
    if ($inc -eq 0) {
        $sep = ""
    }
    else {
        $sep = ","
    }
    $nxt = $i * 7 + $inc
    $disp += $sep + $nxt.ToString()
    }
    $sttm = get-date -Format "yyyy-MM-dd HH:mm:ss"
    python genTMplyrmtchup.py ${disp} # | Select-Object -Last 3
    $entm = get-date -Format "yyyy-MM-dd HH:mm:ss"; Write-Output "set ${disp} ran ${sttm} - ${entm}"
}