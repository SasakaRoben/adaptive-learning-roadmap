#!/bin/bash
# Database initialization script
# This script runs all SQL migrations in the correct order

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Database Initialization Script ===${NC}"

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo -e "${RED}ERROR: DATABASE_URL environment variable is not set${NC}"
    echo "Please set DATABASE_URL with your PostgreSQL connection string"
    echo "Example: export DATABASE_URL='postgresql://user:password@host:5432/dbname'"
    exit 1
fi

echo -e "${YELLOW}Using DATABASE_URL: ${DATABASE_URL%%@*}@***${NC}"

# Check if psql is available
if ! command -v psql &> /dev/null; then
    echo -e "${RED}ERROR: psql command not found${NC}"
    echo "Please install PostgreSQL client tools"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SQL_DIR="$SCRIPT_DIR/backend/sql"

# Check if SQL directory exists
if [ ! -d "$SQL_DIR" ]; then
    echo -e "${RED}ERROR: SQL directory not found at $SQL_DIR${NC}"
    exit 1
fi

# Array of SQL files in the order they should be executed
SQL_FILES=(
    "learning_tables.sql"
    "assessment_schema.sql"
    "learning_resources.sql"
    "user_registration.sql"
)

# Test database connection
echo -e "\n${YELLOW}Testing database connection...${NC}"
if ! psql "$DATABASE_URL" -c "SELECT 1;" > /dev/null 2>&1; then
    echo -e "${RED}ERROR: Cannot connect to database${NC}"
    echo "Please check your DATABASE_URL and ensure the database server is running"
    exit 1
fi
echo -e "${GREEN}✓ Database connection successful${NC}"

# Run each SQL file
echo -e "\n${YELLOW}Running migrations...${NC}"
for sql_file in "${SQL_FILES[@]}"; do
    SQL_PATH="$SQL_DIR/$sql_file"
    
    if [ ! -f "$SQL_PATH" ]; then
        echo -e "${RED}ERROR: SQL file not found: $SQL_PATH${NC}"
        exit 1
    fi
    
    echo -e "\n${YELLOW}Running: $sql_file${NC}"
    if psql "$DATABASE_URL" -f "$SQL_PATH"; then
        echo -e "${GREEN}✓ Successfully executed: $sql_file${NC}"
    else
        echo -e "${RED}✗ Failed to execute: $sql_file${NC}"
        exit 1
    fi
done

echo -e "\n${GREEN}=== Database initialization completed successfully! ===${NC}"
echo -e "You can now start the application."
