# Muler Full-Stack Docker Deployment

## Overview
Your Muler application is now fully containerized and can be deployed with a single command. The entire stack includes:

- **Flask Application** - Running on port 5001
- **MySQL Database** - Running on port 3306  
- **phpMyAdmin** - Running on port 8081

## Quick Start
```bash
# 1. Copy environment template and configure
cp .env.example .env
# Edit .env with your actual values

# 2. Start the entire stack
docker compose up -d

# Stop the stack
docker compose down

# View logs
docker compose logs -f
```

## Environment Configuration
All configuration is managed through the `.env` file. Copy the example template to get started:

```bash
cp .env.example .env
```

Then edit `.env` with your actual values:

```env
# Database Configuration
MYSQL_ROOT_PASSWORD=your_root_password_here
MYSQL_DATABASE=your_database_name
MYSQL_USER=your_database_user
MYSQL_PASSWORD=your_database_password
MYSQL_PORT=3306

# Application Ports
FLASK_PORT=5001
PHPMYADMIN_PORT=8081

# Flask Configuration
FLASK_ENV=production
```

## Services Access
- **Main Application**: http://localhost:5001
- **Database Admin**: http://localhost:8081
- **Database Connection**: `mysql://muler_user:muler_password@localhost:3306/muler`

## Files Cleaned Up
The following unused files were removed during containerization:

### Removed Files:
- `db_setup.py` - Replaced by Docker database initialization
- `test_db_connection.py` - No longer needed with Docker
- `.venv/` - Virtual environment replaced by Docker containers
- `muler/database/muler.db` - SQLite files replaced by MySQL
- `muler/database/test.db` - SQLite test files replaced by MySQL
- `tests/test.db` - SQLite test files replaced by MySQL

### Current Project Structure:
```
muler/
├── .env                    # Environment configuration
├── docker-compose.yml     # Docker orchestration
├── Dockerfile             # Flask app container
├── requirements.txt       # Python dependencies
├── muler/                 # Flask application
│   ├── app.py
│   ├── models.py
│   ├── query.py
│   ├── static/
│   ├── templates/
│   └── database/
│       ├── correction.py
│       ├── regex.py
│       └── xml2sqlite3.py
└── tests/                 # Test files
```

## Key Improvements
1. **Environment Variables**: Centralized configuration in `.env` file
2. **Security**: Database credentials managed through environment variables
3. **Portability**: Single command deployment across different environments
4. **Maintainability**: Clean project structure with unused files removed
5. **Scalability**: Docker containers can be easily scaled and managed

## Next Steps
- The application is ready for production deployment
- Database is persistent across container restarts
- All language switching and search functionality is operational
