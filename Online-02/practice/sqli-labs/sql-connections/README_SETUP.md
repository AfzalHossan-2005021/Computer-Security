# Database Setup Instructions

## Welcome Dhakkan!

I've created complete database setup scripts for your SQL injection labs. Here's how to use them:

## Files Created:

### 1. **setup-db-complete.php** - Web Interface
- **Purpose**: Complete HTML interface for database setup
- **Usage**: Open in web browser
- **URL**: `http://localhost/sqli-labs/sql-connections/setup-db-complete.php`
- **Features**: 
  - Beautiful HTML interface with your "Welcome Dhakkan" theme
  - Real-time progress display
  - Error handling and feedback

### 2. **run-setup.php** - Command Line Version
- **Purpose**: Direct PHP script execution
- **Usage**: Run from command line
- **Command**: `php run-setup.php`
- **Features**:
  - Clean terminal output
  - Progress tracking
  - Error reporting

## What Gets Created:

### Security Database:
- **users table**: 13 user records with usernames and passwords
- **emails table**: 8 email records
- **uagents table**: For user agent injection testing
- **referers table**: For referer header injection testing

### Sample Users Created:
```
ID | Username  | Password
1  | Dumb      | Dumb
2  | Angelina  | I-kill-you
3  | Dummy     | p@ssword
4  | secure    | crappy
5  | stupid    | stupidity
6  | superman  | genious
7  | batman    | mob!le
8  | admin     | admin
9  | admin1    | admin1
10 | admin2    | admin2
11 | admin3    | admin3
12 | dhakkan   | dumbo
14 | admin4    | admin4
```

### Sample Emails Created:
```
ID | Email
1  | Dumb@dhakkan.com
2  | Angel@iloveu.com
3  | Dummy@dhakkan.local
4  | secure@dhakkan.local
5  | stupid@dhakkan.local
6  | superman@dhakkan.local
7  | batman@dhakkan.local
8  | admin@dhakkan.com
```

## How to Run:

### Option 1: Web Interface
1. Start your web server (Apache/Nginx)
2. Navigate to: `http://localhost/sqli-labs/sql-connections/setup-db-complete.php`
3. Watch the setup progress in your browser

### Option 2: Command Line
1. Open terminal
2. Navigate to the directory: `cd /home/afzal/sqli-labs/sql-connections`
3. Run: `php run-setup.php`
4. Watch the progress in terminal

## Database Configuration:

Make sure your `db-creds.inc` file has the correct settings:
```php
<?php
$dbuser = 'root';           // Your MySQL username
$dbpass = '';               // Your MySQL password
$dbname = "security";       // Main database name
$host = 'localhost';        // MySQL host
$dbname1 = "challenges";    // Challenges database name
?>
```

## Features:

✅ **Modern MySQLi**: Uses MySQLi instead of deprecated mysql_* functions
✅ **UTF-8 Support**: Proper character encoding
✅ **Error Handling**: Comprehensive error reporting
✅ **Progress Tracking**: Real-time setup progress
✅ **Clean Interface**: Beautiful dark theme matching your style
✅ **Challenges Database**: Automatic setup of challenges database

## Next Steps:

1. Run the setup script (web or command line)
2. Verify successful creation of both databases
3. Start practicing SQL injection with the provided data
4. Use credentials like `admin/admin` for testing

## Troubleshooting:

- **Connection Error**: Check MySQL service is running
- **Permission Error**: Ensure MySQL user has CREATE/DROP privileges
- **Database Already Exists**: Script will drop and recreate databases
- **Character Set Issues**: Script uses utf8mb4 for better compatibility

Ready to hack! 🚀
