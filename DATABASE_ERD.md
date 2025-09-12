# Muler Database - Entity Relationship Diagram (ERD)

## Database Schema Overview

The Muler application uses a normalized MySQL database with 4 main tables to store DrugBank pharmaceutical data.

## ERD Diagram

```mermaid
erDiagram
    name {
        varchar(10) drugbank_id PK "Primary Key - DrugBank ID"
        text name "Drug Name (Generic)"
    }

    pharm {
        varchar(10) drugbank_id PK,FK "Primary Key & Foreign Key"
        text pd "Pharmacodynamics"
        text mech "Mechanism of Action"
        text ind "Indications"
        text d_class "Drug Classification"
    }

    product {
        varchar(10) drugbank_id FK "Foreign Key to name table"
        text product "Commercial Product Names"
    }

    synonym {
        varchar(10) drugbank_id FK "Foreign Key to name table"
        text synonym "Drug Synonyms/Aliases"
    }

    name ||--|| pharm : "1:1 relationship"
    name ||--o{ product : "1:many relationship"
    name ||--o{ synonym : "1:many relationship"
```

## Docker Container Architecture & Port Mapping

```mermaid
graph TB
    subgraph "Host System (macOS)"
        Browser[Web Browser]
        Admin[Database Admin]
        Browser --> |"HTTP :5001"| AppPort[localhost:5001]
        Admin --> |"HTTP :8081"| PHPPort[localhost:8081]
    end

    subgraph "Docker Network: muler_network"
        subgraph "Flask Container"
            FlaskApp[Flask Application<br/>muler_flask<br/>Internal Port: 5000]
        end

        subgraph "MySQL Container"
            MySQL[MySQL Database<br/>muler_mysql<br/>Internal Port: 3306<br/>External Port: 3306]
        end

        subgraph "phpMyAdmin Container"
            PHPMyAdmin[phpMyAdmin<br/>muler_phpmyadmin<br/>Internal Port: 80<br/>External Port: 8081]
        end

        FlaskApp --> |"mysql://mysql:3306<br/>DATABASE_URL"| MySQL
        PHPMyAdmin --> |"PMA_HOST=mysql<br/>PMA_PORT=3306"| MySQL
    end

    subgraph "Docker Volumes"
        MySQLData[mysql_data<br/>Persistent Storage<br/>/var/lib/mysql]
        MySQL -.-> MySQLData
    end

    AppPort --> |"Port Mapping<br/>5001:5000"| FlaskApp
    PHPPort --> |"Port Mapping<br/>8081:80"| PHPMyAdmin

    subgraph "Environment Variables"
        EnvVars[".env Configuration<br/>MYSQL_ROOT_PASSWORD<br/>MYSQL_DATABASE<br/>MYSQL_USER<br/>MYSQL_PASSWORD<br/>FLASK_PORT=5001<br/>PHPMYADMIN_PORT=8081<br/>MYSQL_PORT=3306"]
    end

    FlaskApp -.-> EnvVars
    MySQL -.-> EnvVars
    PHPMyAdmin -.-> EnvVars
```

## Tech Stack Overview

### **Backend Technologies**

- **Framework**: Flask 2.3.3 (Python Web Framework)
- **Database**: MySQL 8.0 (Production Database Server)
- **Database Driver**: PyMySQL 1.1.1 (MySQL connector for Python)
- **Security**: cryptography>=3.4.8 (MySQL authentication & encryption)
- **ORM/Database Access**: SQLAlchemy (Database abstraction layer)

### **Frontend Technologies**

- **Template Engine**: Jinja2 (Flask built-in templating)
- **Styling**: CSS3 + Custom Stylesheets
- **JavaScript**: Vanilla JavaScript (Dynamic interactions)
- **Internationalization**: Flask-Babel 4.0.0 (Multi-language support)

### **Infrastructure & DevOps**

- **Containerization**: Docker & Docker Compose
- **Base Image**: python:3.12-slim (Debian-based)
- **Database Admin**: phpMyAdmin (Web-based MySQL management)
- **Process Management**: Python built-in WSGI
- **Networking**: Docker Bridge Network

### **Development & Build Tools**

- **Package Manager**: pip (Python package installer)
- **Environment Management**: .env file configuration
- **Version Control**: Git
- **Registry**: Docker Hub (exzqqq/muler:latest)

### **Key Dependencies**

```
Flask==2.3.3                 # Web framework
Flask-Babel==4.0.0          # Internationalization
PyMySQL==1.1.1              # MySQL connector
cryptography>=3.4.8         # Security & encryption
fuzzywuzzy==0.18.0          # Fuzzy string matching
googletrans==4.0.0rc1       # Translation services
Babel==2.14.0               # Localization utilities
```

### **System Dependencies**

```dockerfile
gcc                          # Compiler for native extensions
default-libmysqlclient-dev   # MySQL client development files
pkg-config                   # Package configuration utility
```

### **Production Architecture**

- **Database Engine**: InnoDB (ACID compliance, foreign keys)
- **Character Encoding**: UTF8MB4 (Full Unicode support)
- **Collation**: utf8mb4_general_ci (Case-insensitive)
- **Data Persistence**: Docker volumes (mysql_data)

## Container Connection Details

### **Port Mapping Summary**

| Service    | Container Name   | Internal Port | External Port | Protocol |
| ---------- | ---------------- | ------------- | ------------- | -------- |
| Flask App  | muler_flask      | 5000          | 5001          | HTTP     |
| MySQL      | muler_mysql      | 3306          | 3306          | TCP      |
| phpMyAdmin | muler_phpmyadmin | 80            | 8081          | HTTP     |

### **Network Connections**

1. **Flask ↔ MySQL**

   - Connection: `mysql+pymysql://user:password@mysql:3306/muler`
   - Protocol: MySQL Protocol over TCP
   - Service Discovery: Docker DNS (mysql hostname)

2. **phpMyAdmin ↔ MySQL**

   - Connection: `PMA_HOST=mysql`, `PMA_PORT=3306`
   - Protocol: MySQL Protocol over TCP
   - Authentication: Uses same credentials as Flask app

3. **External Access**
   - **Application**: `http://localhost:5001` → Flask Container
   - **Database Admin**: `http://localhost:8081` → phpMyAdmin Container
   - **Direct DB Access**: `mysql://localhost:3306` → MySQL Container

### **Docker Network Configuration**

```yaml
# Network Definition
networks:
  muler_network:
    driver: bridge

# Service Network Assignment
services:
  mysql:
    networks: [muler_network]
  phpmyadmin:
    networks: [muler_network]
  flask_app:
    networks: [muler_network]
```

### **Volume Mounting**

- **MySQL Data**: `mysql_data:/var/lib/mysql` (Persistent storage)
- **Application Code**: `.:/app` (Development volume mount)
- **Database Init**: `./muler/database/muler.sql:/docker-entrypoint-initdb.d/muler.sql:ro`

## Database Tables Detail

### 1. **`name` Table** (Primary Entity)

- **Purpose**: Stores primary drug information
- **Primary Key**: `drugbank_id` (VARCHAR(10))
- **Columns**:
  - `drugbank_id`: Unique DrugBank identifier (e.g., "DB00001")
  - `name`: Generic/official drug name (TEXT)

### 2. **`pharm` Table** (Pharmacological Information)

- **Purpose**: Stores detailed pharmacological data
- **Primary Key**: `drugbank_id` (also Foreign Key)
- **Relationship**: 1:1 with `name` table
- **Columns**:
  - `drugbank_id`: Links to name table
  - `pd`: Pharmacodynamics description
  - `mech`: Mechanism of action
  - `ind`: Medical indications
  - `d_class`: Drug classification

### 3. **`product` Table** (Commercial Products)

- **Purpose**: Stores commercial/brand names
- **Foreign Key**: `drugbank_id` → `name.drugbank_id`
- **Relationship**: 1:Many with `name` table
- **Columns**:
  - `drugbank_id`: Links to name table
  - `product`: Commercial product name

### 4. **`synonym` Table** (Drug Synonyms)

- **Purpose**: Stores alternative names and synonyms
- **Foreign Key**: `drugbank_id` → `name.drugbank_id`
- **Relationship**: 1:Many with `name` table
- **Columns**:
  - `drugbank_id`: Links to name table
  - `synonym`: Alternative drug name

## Database Characteristics

### **Storage Engine**: InnoDB

- Supports foreign key constraints
- ACID compliance
- Row-level locking

### **Character Set**: UTF8MB4

- Full Unicode support
- Supports Thai language characters
- Emoji and special character support

### **Collation**: utf8mb4_general_ci

- Case-insensitive comparisons
- General Unicode collation rules

## Data Relationships

```
name (1) ←→ (1) pharm        [One drug has one pharmacological profile]
name (1) ←→ (0..n) product   [One drug can have multiple commercial products]
name (1) ←→ (0..n) synonym   [One drug can have multiple synonyms/aliases]
```

## Search Strategy

The application searches across multiple tables:

1. **Primary Search**: `name.name` field
2. **Secondary Search**: `synonym.synonym` field
3. **Product Search**: `product.product` field
4. **Results Join**: All pharmacological data from `pharm` table

## Database Performance

- **Primary Keys**: Clustered indexes on all `drugbank_id` fields
- **Foreign Keys**: Automatic indexes for referential integrity
- **Text Fields**: Full-text search capabilities for drug names and descriptions

## Data Source

- **Origin**: DrugBank XML dataset
- **License**: CC BY-NC 4.0
- **Processing**: Converted from XML to normalized MySQL schema
- **Updates**: Manual import from DrugBank releases

---

_This ERD represents the complete data model for the Muler Drug Information Search Application_
