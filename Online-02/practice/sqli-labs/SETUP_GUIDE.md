# SQL Injection Labs - Database Setup Guide

## Files Created/Updated

### 1. **complete-setup.php** - Web Interface Setup
- **Purpose**: Full HTML interface for database setup
- **Features**: 
  - Beautiful dark theme interface
  - Real-time setup progress
  - Error handling with visual feedback
  - Creates both security and challenges databases
- **Usage**: Open in web browser: `http://localhost/sqli-labs/sql-connections/complete-setup.php`

### 2. **setup-complete-cli.php** - Command Line Setup
- **Purpose**: Command-line database setup
- **Features**:
  - Clean terminal output
  - Progress tracking
  - Data summary
  - Sample user listing
- **Usage**: Run from terminal: `php setup-complete-cli.php`

### 3. **test-setup.php** - Database Testing
- **Purpose**: Verify database setup integrity
- **Features**:
  - Connection testing
  - Table verification
  - Data validation
  - Sample query testing
- **Usage**: Run from terminal: `php test-setup.php`

## Database Structure

### Security Database Tables:
- **users**: Login credentials for injection testing
- **emails**: Email addresses for injection testing
- **uagents**: User agent strings and IP addresses
- **referers**: Referer URLs and IP addresses

### Challenges Database:
- **Dynamic table**: Random table name with session management

## Sample Data

### Users Table (13 records):
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

### Emails Table (8 records):
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

## Quick Start

1. **Configure database credentials** in `db-creds.inc`:
   ```php
   $dbuser = 'root';
   $dbpass = '';
   $dbname = "security";
   $host = 'localhost';
   $dbname1 = "challenges";
   ```

2. **Run setup** (choose one):
   - Web: `complete-setup.php`
   - CLI: `php setup-complete-cli.php`

3. **Test setup**:
   ```bash
   php test-setup.php
   ```

4. **Start practicing** SQL injection on the labs!

## Troubleshooting

### Common Issues:
1. **Connection Failed**: Check MySQL credentials in `db-creds.inc`
2. **Permission Denied**: Ensure MySQL user has CREATE/DROP privileges
3. **Character Set Issues**: Make sure MySQL supports utf8mb4

### Error Messages:
- `Could not connect to DB`: Check MySQL service and credentials
- `Error creating database`: Check user privileges
- `Error creating Table`: Check database exists and user permissions

## Modern Features

✅ **MySQLi Support**: Compatible with PHP 7.0+
✅ **UTF-8 Support**: Proper character encoding
✅ **Error Handling**: Comprehensive error reporting
✅ **Clean Code**: Well-structured and maintainable
✅ **Security**: Updated connection methods
✅ **Backward Compatible**: Works with existing labs

## Next Steps

After successful setup:
1. Navigate to your SQL injection labs
2. Start with Less-1 for basic injection
3. Use the provided credentials for testing
4. Practice different injection techniques

Happy hacking! 🚀
