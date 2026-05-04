<?php
/**
 * Fix File Operations Script for SQLi-Labs
 * 
 * This script fixes file operation issues in all Less-n folders
 * by properly handling fopen, fwrite, and fclose operations
 * 
 * Usage: php fix_file_operations.php
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "=== SQLi-Labs File Operations Fix Script ===\n";
echo "Fixing file operations in all Less-n folders...\n\n";

// Get all Less-n directories
$lessDirs = glob(__DIR__ . '/Less-*', GLOB_ONLYDIR);
sort($lessDirs, SORT_NATURAL);

$totalDirs = count($lessDirs);
$fixedDirs = 0;

echo "Found $totalDirs Less-n directories to process.\n\n";

foreach ($lessDirs as $lessDir) {
    $lessDirName = basename($lessDir);
    echo "Processing $lessDirName...\n";
    
    // Get all PHP files in the directory
    $phpFiles = glob($lessDir . '/*.php');
    
    if (empty($phpFiles)) {
        echo "  No PHP files found in $lessDirName\n";
        continue;
    }
    
    $filesFixed = 0;
    
    foreach ($phpFiles as $phpFile) {
        $fileName = basename($phpFile);
        
        // Read the current file content
        $content = file_get_contents($phpFile);
        if ($content === false) {
            echo "  ERROR: Cannot read $fileName\n";
            continue;
        }
        
        $originalContent = $content;
        
        // Pattern 1: Fix sequences like:
        // $fp=@fopen('result.txt','a');
        // if($fp) fwrite($fp,'...');
        // if($fp) fclose($fp);
        $pattern1 = '/\$fp=@fopen\(\'result\.txt\',\'a\'\);\s*if\(\$fp\)\s*fwrite\(\$fp,([^;]+)\);\s*if\(\$fp\)\s*fclose\(\$fp\);/s';
        $replacement1 = '$fp=@fopen(\'result.txt\',\'a\');
if ($fp) {
    fwrite($fp,$1);
    fclose($fp);
}';
        
        $content = preg_replace($pattern1, $replacement1, $content);
        
        // Pattern 2: Fix sequences like:
        // $fp=@fopen("result.txt","a");
        // if($fp) fwrite($fp,...);
        // if($fp) fclose($fp);
        $pattern2 = '/\$fp=@fopen\("result\.txt","a"\);\s*if\(\$fp\)\s*fwrite\(\$fp,([^;]+)\);\s*if\(\$fp\)\s*fclose\(\$fp\);/s';
        $replacement2 = '$fp=@fopen("result.txt","a");
if ($fp) {
    fwrite($fp,$1);
    fclose($fp);
}';
        
        $content = preg_replace($pattern2, $replacement2, $content);
        
        // Pattern 3: Fix multi-line file operations
        $pattern3 = '/\$fp=@fopen\(\'result\.txt\',\'a\'\);\s*if\(\$fp\)\s*fwrite\(\$fp,([^;]+)\);\s*if\(\$fp\)\s*fwrite\(\$fp,([^;]+)\);\s*if\(\$fp\)\s*fclose\(\$fp\);/s';
        $replacement3 = '$fp=@fopen(\'result.txt\',\'a\');
if ($fp) {
    fwrite($fp,$1);
    fwrite($fp,$2);
    fclose($fp);
}';
        
        $content = preg_replace($pattern3, $replacement3, $content);
        
        // Pattern 4: Fix already partially fixed ones
        $pattern4 = '/\$fp=@fopen\(\'result\.txt\',\'a\'\);\s*if\s*\(\$fp\)\s*\{\s*if\(\$fp\)\s*fwrite\(\$fp,([^;]+)\);\s*if\(\$fp\)\s*fclose\(\$fp\);\s*\}/s';
        $replacement4 = '$fp=@fopen(\'result.txt\',\'a\');
if ($fp) {
    fwrite($fp,$1);
    fclose($fp);
}';
        
        $content = preg_replace($pattern4, $replacement4, $content);
        
        // Only write if content changed
        if ($content !== $originalContent) {
            if (file_put_contents($phpFile, $content) !== false) {
                echo "  ✓ Fixed $fileName\n";
                $filesFixed++;
            } else {
                echo "  ERROR: Cannot write to $fileName\n";
            }
        }
    }
    
    if ($filesFixed > 0) {
        echo "  ✓ Fixed $filesFixed files in $lessDirName\n";
        $fixedDirs++;
    } else {
        echo "  - No files needed fixing in $lessDirName\n";
    }
    
    echo "\n";
}

echo "=== File Operations Fix Complete ===\n";
echo "Total directories: $totalDirs\n";
echo "Fixed directories: $fixedDirs\n";

echo "\nNow fixing file permissions for result.txt files...\n";

// Fix permissions for existing result.txt files and create template
foreach ($lessDirs as $lessDir) {
    $resultFile = $lessDir . '/result.txt';
    
    // Create result.txt if it doesn't exist
    if (!file_exists($resultFile)) {
        @file_put_contents($resultFile, '');
    }
    
    // Set proper permissions
    @chmod($resultFile, 0666);
}

echo "File permissions fixed.\n";
echo "\nRecommended next steps:\n";
echo "1. Test the labs again\n";
echo "2. Check for any remaining issues\n";

?>
