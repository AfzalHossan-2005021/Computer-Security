# SQL Injection Labs - Complete Setup Guide

## 🎯 Welcome Dhakkan!

This guide provides complete instructions for setting up and running SQL injection labs with modern PHP and MySQL.

## 🔧 What Was Fixed

### Original Problems:
- **Deprecated MySQL Functions**: Code used `mysql_*` functions removed in PHP 7.0+
- **PHP Not Installed**: System didn't have PHP installed
- **Missing Web Server**: Apache wasn't configured
- **Database Connection Issues**: Old connection methods not working
- **Function Conflicts**: Duplicate function names causing errors

### Solutions Applied:
- ✅ **Installed PHP 8.3** with MySQL support
- ✅ **Updated all code** to use MySQLi
- ✅ **Configured Apache2** web server
- ✅ **Fixed function conflicts** in setup scripts
- ✅ **Created proper web directory** structure
- ✅ **Updated character sets** to UTF-8

## 📋 Prerequisites

### System Requirements:
- Ubuntu 24.04 LTS (or similar)
- Root/sudo access
- Internet connection for package installation

### Software Installed:
- **PHP 8.3.6** with MySQLi extension
- **MySQL 8.0** database server
- **Apache2** web server

## 🚀 Installation Steps

### 1. Install Required Packages
```bash
sudo apt update
sudo apt install php php-mysql apache2 mysql-server -y
```

### 2. Start Services
```bash
sudo systemctl start apache2 mysql
sudo systemctl enable apache2 mysql
```

### 3. Create Web Directory
```bash
sudo mkdir -p /var/www/html
sudo ln -sf /home/afzal/sqli-labs /var/www/html/sqli-labs
```

### 4. Verify Installation
```bash
php --version
sudo systemctl status apache2
sudo systemctl status mysql
```

## 📁 Files Created/Updated

### 1. **setup-db-complete.php** - Web Interface Setup
- **Location**: `/home/afzal/sqli-labs/sql-connections/setup-db-complete.php`
- **Purpose**: Complete HTML interface for database setup
- **Features**: 
  - Beautiful dark theme with "Welcome Dhakkan" styling
  - Real-time setup progress display
  - Comprehensive error handling
  - Creates both security and challenges databases

### 2. **run-setup.php** - Command Line Setup
- **Location**: `/home/afzal/sqli-labs/sql-connections/run-setup.php`
- **Purpose**: Direct PHP script execution for database setup
- **Features**:
  - Clean terminal output
  - Progress tracking
  - Error reporting
  - Database summary

### 3. **test-php-mysql.php** - Testing Script
- **Location**: `/home/afzal/sqli-labs/sql-connections/test-php-mysql.php`
- **Purpose**: Verify PHP and MySQL connectivity
- **Features**:
  - PHP version check
  - MySQL connection test
  - Database verification
  - User count display

### 4. **Updated Core Files**
- **setup-db.php** - Converted to MySQLi
- **setup-db-challenge.php** - Fixed function conflicts
- **functions.php** - Complete MySQLi rewrite
- **sql-connect.php** - Updated connection methods
- **sql-connect-1.php** - Updated connection methods

## 🗄️ Database Structure

### Security Database Tables:

#### 1. **users** Table (13 records)
```sql
CREATE TABLE users (
    id int(3) NOT NULL AUTO_INCREMENT,
    username varchar(20) NOT NULL,
    password varchar(20) NOT NULL,
    PRIMARY KEY (id)
);
```

**Sample Data:**
| ID | Username  | Password    |
|----|-----------|-------------|
| 1  | Dumb      | Dumb        |
| 2  | Angelina  | I-kill-you  |
| 3  | Dummy     | p@ssword    |
| 4  | secure    | crappy      |
| 5  | stupid    | stupidity   |
| 6  | superman  | genious     |
| 7  | batman    | mob!le      |
| 8  | admin     | admin       |
| 9  | admin1    | admin1      |
| 10 | admin2    | admin2      |
| 11 | admin3    | admin3      |
| 12 | dhakkan   | dumbo       |
| 14 | admin4    | admin4      |

#### 2. **emails** Table (8 records)
```sql
CREATE TABLE emails (
    id int(3) NOT NULL AUTO_INCREMENT,
    email_id varchar(30) NOT NULL,
    PRIMARY KEY (id)
);
```

**Sample Data:**
| ID | Email                    |
|----|--------------------------|
| 1  | Dumb@dhakkan.com        |
| 2  | Angel@iloveu.com        |
| 3  | Dummy@dhakkan.local     |
| 4  | secure@dhakkan.local    |
| 5  | stupid@dhakkan.local    |
| 6  | superman@dhakkan.local  |
| 7  | batman@dhakkan.local    |
| 8  | admin@dhakkan.com       |

#### 3. **uagents** Table
```sql
CREATE TABLE uagents (
    id int(3) NOT NULL AUTO_INCREMENT,
    uagent varchar(256) NOT NULL,
    ip_address varchar(35) NOT NULL,
    username varchar(20) NOT NULL,
    PRIMARY KEY (id)
);
```

#### 4. **referers** Table
```sql
CREATE TABLE referers (
    id int(3) NOT NULL AUTO_INCREMENT,
    referer varchar(256) NOT NULL,
    ip_address varchar(35) NOT NULL,
    PRIMARY KEY (id)
);
```

### Challenges Database:
- **Dynamic Table**: Random table name (e.g., `QPJS1G4BZC`)
- **Columns**: id, sessid, secret_key, tryy
- **Purpose**: Advanced challenge scenarios

## 🎮 How to Use

### Option 1: Web Interface
1. **Access URL**: `http://localhost/sqli-labs/sql-connections/setup-db-complete.php`
2. **Features**: Beautiful interface with real-time progress
3. **Output**: HTML formatted with dark theme

### Option 2: Command Line
1. **Command**: `php /home/afzal/sqli-labs/sql-connections/run-setup.php`
2. **Features**: Clean terminal output
3. **Output**: Text-based progress tracking

### Option 3: Test Connection
1. **URL**: `http://localhost/sqli-labs/sql-connections/test-php-mysql.php`
2. **Purpose**: Verify everything is working
3. **Shows**: PHP version, MySQL status, database info

## 🔍 Testing & Verification

### 1. Test Database Setup
```bash
# Command line test
php /home/afzal/sqli-labs/sql-connections/run-setup.php

# Web interface test
curl -s http://localhost/sqli-labs/sql-connections/setup-db-complete.php
```

### 2. Verify Database Creation
```bash
mysql -u root -p
```
```sql
SHOW DATABASES;
USE security;
SHOW TABLES;
SELECT COUNT(*) FROM users;
SELECT * FROM users LIMIT 5;
```

### 3. Test Web Interface
```bash
curl -s http://localhost/sqli-labs/sql-connections/test-php-mysql.php
```

## 🛠️ Configuration

### Database Credentials (`db-creds.inc`)
```php
<?php
$dbuser = 'root';           // MySQL username
$dbpass = '';               // MySQL password (empty for default)
$dbname = "security";       // Main database name
$host = 'localhost';        // MySQL host
$dbname1 = "challenges";    // Challenges database name
?>
```

### Web Server Configuration
- **Document Root**: `/var/www/html/`
- **Project Link**: `/var/www/html/sqli-labs -> /home/afzal/sqli-labs`
- **Access URL**: `http://localhost/sqli-labs/`

## 🔧 Modern Features

### Code Improvements:
✅ **MySQLi Support**: Compatible with PHP 7.0+ and PHP 8.x
✅ **UTF-8 Character Set**: Proper Unicode support (utf8mb4)
✅ **Error Handling**: Comprehensive error reporting and logging
✅ **Security**: Updated connection methods and practices
✅ **Maintainability**: Clean, well-structured code
✅ **Compatibility**: Works with modern MySQL/MariaDB versions

### Interface Improvements:
✅ **Dark Theme**: Professional black background styling
✅ **Real-time Feedback**: Progress indicators and status messages
✅ **Error Display**: Clear error messages with solutions
✅ **Responsive Design**: Works on different screen sizes
✅ **Multiple Options**: Web interface and command line support

## 🎯 SQL Injection Lab Usage

### Getting Started:
1. **Run Setup**: Use either web interface or command line
2. **Verify Creation**: Check that databases and tables exist
3. **Start Labs**: Navigate to individual lab exercises
4. **Test Credentials**: Use provided usernames and passwords

### Common Test Credentials:
- **admin/admin** - Basic admin access
- **dhakkan/dumbo** - Named after the welcome message
- **Dumb/Dumb** - Simple test account
- **secure/crappy** - Ironic security test

### Lab Structure:
- **Less-1 to Less-65**: Progressive difficulty levels
- **Each Lab**: Focuses on different injection techniques
- **Challenges**: Advanced scenarios with dynamic tables

## 🚨 Troubleshooting

### Common Issues:

#### 1. **"PHP code not executing"**
- **Cause**: PHP not installed or Apache not configured
- **Solution**: Run installation commands above

#### 2. **"Connection failed"**
- **Cause**: MySQL not running or wrong credentials
- **Solution**: 
  ```bash
  sudo systemctl start mysql
  sudo systemctl status mysql
  ```

#### 3. **"Database not found"**
- **Cause**: Setup script not run successfully
- **Solution**: Run setup script again

#### 4. **"Permission denied"**
- **Cause**: File permissions or MySQL user privileges
- **Solution**: 
  ```bash
  sudo chown -R www-data:www-data /var/www/html/sqli-labs
  sudo chmod -R 755 /var/www/html/sqli-labs
  ```

#### 5. **"Function redeclared"**
- **Cause**: Function conflicts between files
- **Solution**: Use updated files provided (fixed)

### Service Commands:
```bash
# Start services
sudo systemctl start apache2 mysql

# Stop services
sudo systemctl stop apache2 mysql

# Restart services
sudo systemctl restart apache2 mysql

# Check status
sudo systemctl status apache2 mysql
```

## 📊 Expected Output

### Successful Setup Output:
```
Welcome Dhakkan
SETTING UP THE DATABASE SCHEMA AND POPULATING DATA IN TABLES:

[*]...................Old database 'SECURITY' purged if exists
[*]...................Creating New database 'SECURITY' successfully
[*]...................Creating New Table 'USERS' successfully
[*]...................Creating New Table 'EMAILS' successfully
[*]...................Creating New Table 'UAGENTS' successfully
[*]...................Creating New Table 'REFERERS' successfully
[*]...................Inserted data correctly into table 'USERS'
[*]...................Inserted data correctly into table 'EMAILS'

[*] SECURITY DATABASE SETUP COMPLETED!
[*] Setting up challenges database...

[*]...................Old database purged if exists
[*]...................Creating New database successfully
[*]...................Creating New Table 'RANDOMNAME' successfully
[*]...................Inserted data correctly into table 'RANDOMNAME'
[*]...................Inserted secret key 'secret_XXXX' into table

[*] ALL DATABASE SETUP COMPLETED SUCCESSFULLY!
[*] You can now run your SQL injection labs.
```

## 🎉 Success Verification

### Database Created Successfully:
- ✅ **Security Database**: 4 tables, 21 total records
- ✅ **Challenges Database**: 1 dynamic table with session data
- ✅ **Test Users**: 13 user accounts for injection testing
- ✅ **Test Emails**: 8 email addresses for testing
- ✅ **Web Interface**: Fully functional with proper styling
- ✅ **Command Line**: Working for server environments

### Ready for SQL Injection Labs:
- ✅ **PHP 8.3** with MySQLi support
- ✅ **MySQL 8.0** with UTF-8 support
- ✅ **Apache2** serving PHP files
- ✅ **Modern Code** compatible with current PHP versions
- ✅ **Comprehensive Testing** tools included

## 🔮 Next Steps

1. **Start with Less-1**: Begin with basic SQL injection
2. **Use Test Credentials**: Try admin/admin, dhakkan/dumbo, etc.
3. **Progress Through Labs**: Each lab teaches different techniques
4. **Practice Regularly**: SQL injection skills need practice
5. **Document Learning**: Keep notes on successful injections

## 📚 Additional Resources

### SQL Injection Types Covered:
- **Union-based**: Combining queries for data extraction
- **Boolean-based**: True/false logic for blind injection
- **Time-based**: Delay-based blind injection
- **Error-based**: Using error messages for information
- **Header-based**: User-Agent, Referer, Cookie injection
- **POST-based**: Form parameter injection

### Learning Path:
1. **Basic Injection** (Less-1 to Less-10)
2. **Advanced Techniques** (Less-11 to Less-20)
3. **Bypass Techniques** (Less-21 to Less-30)
4. **Complex Scenarios** (Less-31 to Less-65)
5. **Challenge Mode** (Challenges database)

---

## 🎯 Final Status: ✅ COMPLETE SUCCESS!

Your SQL injection labs are now **fully functional** with:
- Modern PHP 8.3 compatibility
- Secure MySQLi connections
- Beautiful web interface
- Comprehensive database setup
- Professional error handling
- Complete documentation

**Happy Hacking, Dhakkan!** 🚀

---

*Last updated: July 4, 2025*
*PHP Version: 8.3.6*
*MySQL Version: 8.0*
*Status: Production Ready*
