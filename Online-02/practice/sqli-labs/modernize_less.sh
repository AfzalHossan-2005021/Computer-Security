#!/bin/bash
# Usage: ./modernize_less.sh 5
# This will update all .php files in Less-5

if [ -z "$1" ]; then
  echo "Usage: $0 <LESS_NUMBER>"
  exit 1
fi

DIR="Less-$1"

if [ ! -d "$DIR" ]; then
  echo "Directory $DIR does not exist!"
  exit 2
fi

find "$DIR" -type f -name "*.php" -print0 | while IFS= read -r -d '' file; do
  sed -i "s/mysql_query(\$sql)/mysqli_query(\$GLOBALS['con1'], \$sql)/g" "$file"
  sed -i "s/mysql_fetch_array/mysqli_fetch_array/g" "$file"
  sed -i "s/mysql_error()/mysqli_error(\$GLOBALS['con1'])/g" "$file"
done

echo "All replacements done in $DIR."