<?php
require_once 'log.php';

$baseDir = realpath('/var/www/html');

$language = $_GET['language'] ?? 'languages/english.php';

logEvent("Language parameter accessed: $language");

$filePath = realpath($language);

ob_start();

if ($filePath && strpos($filePath, $baseDir) === 0 && file_exists($filePath)) {
    include($filePath);
} else {
    echo "<p>File not found or access denied: " . htmlspecialchars($language) . "</p>";
    logEvent("Access denied or file not found for: $language");
}
$languageContent = ob_get_clean();
?>



<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The John Hammond Conspiracy</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
     <div class="marquee">
        <p>How can one man have so many interests??!! Dinosaurs, golden age musicians, cybersecurity??!! MAKE IT MAKE SENSE </p>
    </div>
    <nav class="navbar">
        <ul>
            <li><a href="index.php">Home</a></li>
            <li><a href="conspiracy.php">The Conspiracy</a></li>
            <li><a href="upload.php">Upload Evidence</a></li>
            <li><a href="#contact">Contact Us</a></li>
        </ul>
    </nav>

    <div class="navbar">
        <a href="conspiracy.php?language=languages/english.php">English</a> |
        <a href="conspiracy.php?language=languages/french.php">French</a>
    </div>

    <div class="content">
        <?php
        echo $languageContent;
        ?>
    </div>
</body>
</html>
