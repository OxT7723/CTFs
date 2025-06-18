<?php
require_once 'log.php';

$uploadDir = 'uploads/';
$allowedExtensions = ['jpg', 'png', 'gif'];

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['image'])) {
    $originalName = basename($_FILES['image']['name']);
    $fileTmpPath = $_FILES['image']['tmp_name'];
    $fileExtension = strtolower(pathinfo($originalName, PATHINFO_EXTENSION));

    $uniqueName = uniqid() . "_$originalName";
    $uploadPath = $uploadDir . $uniqueName;

    if (in_array($fileExtension, $allowedExtensions)) {
        if (move_uploaded_file($fileTmpPath, $uploadPath)) {
            logEvent("Uploaded file: $uniqueName");
            $message = "Your file <strong>$originalName</strong> has been uploaded successfully! The truth is out there.";
        } else {
            logEvent("Error moving file: $originalName");
            $message = "Something went wrong during the upload. Is someone tampering with the evidence?";
        }
    } else {
        logEvent("Invalid file type attempted: $originalName");
        $message = "The file type you uploaded is not allowed. Are you trying to sabotage the investigation?";
    }
} else {
    $message = "No file uploaded. Do you have evidence, or are you just here to observe?";
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Your John Hammond Images</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="marquee">
        <p>The truth will be uncovered. Upload your evidence now and help us expose the real John Hammond!</p>
    </div>
    <nav class="navbar">
        <ul>
            <li><a href="index.php">Home</a></li>
            <li><a href="conspiracy.php">The Conspiracy</a></li>
            <li><a href="upload.php">Upload Evidence</a></li>
            <li><a href="#contact">Contact Us</a></li>
        </ul>
    </nav>
    <div class="content">
        <h1>Upload Your Images of John Hammond</h1>
        <p>Have you seen John Hammond? The musician, the park owner, the cybersecurity researcher—he can't be all three! Upload any evidence you've found to aid our investigation. Your submissions might hold the key to unraveling the mystery.</p>
        <p>Only images (<strong>JPG, PNG, GIF</strong>) are allowed. All other formats will be rejected to maintain the integrity of our investigation.</p>
        <?php if (isset($message)): ?>
            <p class="status-message"><?= htmlspecialchars($message) ?></p>
        <?php endif; ?>
        <form action="upload.php" method="post" enctype="multipart/form-data">
            <label for="image"><strong>Select your evidence file:</strong></label>
            <input type="file" name="image" id="image" required>
            <button type="submit">Upload Evidence</button>
        </form>
        <p class="footer-text">Your submission will be reviewed by our top conspiracy analysts. Together, we will uncover the truth!</p>
    </div>
</body>
</html>
