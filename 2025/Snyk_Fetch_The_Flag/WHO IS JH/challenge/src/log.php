<?php
$logFile = 'logs/site_log.txt';

/**
 * Logs a message to the centralized log file.
 *
 * @param string $message The message to log.
 */
function logEvent($message) {
    global $logFile;

    if (!is_dir(dirname($logFile))) {
        mkdir(dirname($logFile), 0755, true);
    }

    $timestamp = date('[Y-m-d H:i:s]');
    $formattedMessage = "$timestamp $message\n";

    file_put_contents($logFile, $formattedMessage, FILE_APPEND);
}
?>
