# Docker Database Setup for Muler

This guide will help you set up a MySQL database using Docker for the Muler application.

## Prerequisites

- Docker and Docker Compose installed
- Python virtual environment activated

## Quick Start

### 1. Start the MySQL Database

```bash
# Start MySQL and phpMyAdmin containers
docker-compose up -d

# Check if containers are running
docker-compose ps
```

### 2. Wait for Database Initialization

The database will automatically import the `muler.sql` file. Wait about 30 seconds for the initialization to complete.

### 3. Test the Connection

```bash
# Test MySQL connection
python db_setup.py test-mysql

# If MySQL is working, switch the app to use MySQL
python db_setup.py switch-mysql
```

### 4. Run the Application

```bash
# Run the Flask application
python -m muler.app
```

## Database Access

- **MySQL Database**: `localhost:3306`

  - Database: `muler`
  - Username: `muler_user`
  - Password: `muler_password`

- **phpMyAdmin**: http://localhost:8080
  - Username: `muler_user`
  - Password: `muler_password`

## Useful Commands

```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs mysql

# Access MySQL CLI
docker exec -it muler_mysql mysql -u muler_user -p muler

# Switch back to SQLite (if needed)
python db_setup.py switch-sqlite

# Reset database (removes all data!)
docker-compose down -v
docker-compose up -d
```

## Troubleshooting

1. **Connection refused**: Make sure Docker containers are running
2. **Access denied**: Check username/password in docker-compose.yml
3. **Database not found**: Wait for initialization to complete
4. **Port conflicts**: Change ports in docker-compose.yml if needed

## Environment Variables

You can customize the database settings by editing `docker-compose.yml`:

- `MYSQL_ROOT_PASSWORD`: Root password
- `MYSQL_DATABASE`: Database name
- `MYSQL_USER`: Application user
- `MYSQL_PASSWORD`: Application password
