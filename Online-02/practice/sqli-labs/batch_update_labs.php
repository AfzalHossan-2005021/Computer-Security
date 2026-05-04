<?php
/**
 * Batch Update Script for SQLi-Labs
 * 
 * This script systematically updates all Less-n folders to:
 * 1. Replace mysql_* functions with MySQLi equivalents
 * 2. Fix file logging issues
 * 3. Ensure PHP 8+ compatibility
 * 
 * Usage: php batch_update_labs.php
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "=== SQLi-Labs Batch Update Script ===\n";
echo "Starting modernization of all Less-n folders...\n\n";

// Get all Less-n directories
$lessDirs = glob(__DIR__ . '/Less-*', GLOB_ONLYDIR);
sort($lessDirs, SORT_NATURAL);

$totalDirs = count($lessDirs);
$updatedDirs = 0;
$skippedDirs = 0;
$errorDirs = 0;

echo "Found $totalDirs Less-n directories to process.\n\n";

// MySQL to MySQLi conversion mappings
$mysqlToMysqli = [
    'mysql_query(' => 'mysqli_query($GLOBALS["con1"], ',
    'mysql_fetch_array(' => 'mysqli_fetch_array(',
    'mysql_fetch_row(' => 'mysqli_fetch_row(',
    'mysql_error()' => 'mysqli_error($GLOBALS["con1"])',
    'mysql_real_escape_string(' => 'mysqli_real_escape_string($GLOBALS["con1"], ',
    'mysql_num_rows(' => 'mysqli_num_rows(',
    'mysql_affected_rows()' => 'mysqli_affected_rows($GLOBALS["con1"])',
    'mysql_insert_id()' => 'mysqli_insert_id($GLOBALS["con1"])',
    'mysql_close()' => 'mysqli_close($GLOBALS["con1"])',
];

foreach ($lessDirs as $lessDir) {
    $lessDirName = basename($lessDir);
    echo "Processing $lessDirName...\n";
    
    try {
        // Get all PHP files in the directory
        $phpFiles = glob($lessDir . '/*.php');
        
        if (empty($phpFiles)) {
            echo "  No PHP files found in $lessDirName\n";
            $skippedDirs++;
            continue;
        }
        
        $filesUpdated = 0;
        
        foreach ($phpFiles as $phpFile) {
            $fileName = basename($phpFile);
            echo "  Updating $fileName...\n";
            
            // Read the current file content
            $content = file_get_contents($phpFile);
            if ($content === false) {
                echo "    ERROR: Cannot read $fileName\n";
                continue;
            }
            
            $originalContent = $content;
            
            // Apply MySQL to MySQLi conversions
            foreach ($mysqlToMysqli as $oldFunction => $newFunction) {
                $content = str_replace($oldFunction, $newFunction, $content);
            }
            
            // Fix file logging issues - make it safe with error suppression
            $fileLogPatterns = [
                '/\$fp=fopen\(\'result\.txt\',\'a\'\);/' => '$fp=@fopen(\'result.txt\',\'a\');',
                '/\$fp=fopen\("result\.txt","a"\);/' => '$fp=@fopen("result.txt","a");',
                '/fwrite\(\$fp,/' => 'if($fp) fwrite($fp,',
                '/fclose\(\$fp\);/' => 'if($fp) fclose($fp);',
            ];
            
            foreach ($fileLogPatterns as $pattern => $replacement) {
                $content = preg_replace($pattern, $replacement, $content);
            }
            
            // Additional safety for file operations
            $content = str_replace(
                ['$fp=fopen(', '$fp = fopen('],
                ['$fp=@fopen(', '$fp = @fopen('],
                $content
            );
            
            // Only write if content changed
            if ($content !== $originalContent) {
                if (file_put_contents($phpFile, $content) !== false) {
                    echo "    ✓ Updated $fileName\n";
                    $filesUpdated++;
                } else {
                    echo "    ERROR: Cannot write to $fileName\n";
                }
            } else {
                echo "    - No changes needed for $fileName\n";
            }
        }
        
        if ($filesUpdated > 0) {
            echo "  ✓ Updated $filesUpdated files in $lessDirName\n";
            $updatedDirs++;
        } else {
            echo "  - No files updated in $lessDirName\n";
            $skippedDirs++;
        }
        
    } catch (Exception $e) {
        echo "  ERROR: Failed to process $lessDirName: " . $e->getMessage() . "\n";
        $errorDirs++;
    }
    
    echo "\n";
}

echo "=== Batch Update Complete ===\n";
echo "Total directories: $totalDirs\n";
echo "Updated directories: $updatedDirs\n";
echo "Skipped directories: $skippedDirs\n";
echo "Error directories: $errorDirs\n";

// Create a summary report
$reportFile = __DIR__ . '/batch_update_report.txt';
$report = "SQLi-Labs Batch Update Report\n";
$report .= "Generated: " . date('Y-m-d H:i:s') . "\n\n";
$report .= "Total directories processed: $totalDirs\n";
$report .= "Successfully updated: $updatedDirs\n";
$report .= "Skipped (no changes): $skippedDirs\n";
$report .= "Errors encountered: $errorDirs\n\n";

$report .= "Conversions applied:\n";
foreach ($mysqlToMysqli as $old => $new) {
    $report .= "  $old -> $new\n";
}

$report .= "\nFile logging fixes:\n";
$report .= "  - Added error suppression to fopen() calls\n";
$report .= "  - Added null checks for file operations\n";
$report .= "  - Made file logging safe for PHP 8+\n";

if (file_put_contents($reportFile, $report)) {
    echo "\nDetailed report saved to: batch_update_report.txt\n";
} else {
    echo "\nWARNING: Could not save report file\n";
}

echo "\nRecommended next steps:\n";
echo "1. Test a few key labs manually\n";
echo "2. Run the test script to verify functionality\n";
echo "3. Check Apache error logs for any issues\n";
echo "4. Update documentation if needed\n";

?>
