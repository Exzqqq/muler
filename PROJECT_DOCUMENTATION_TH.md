# Muler - Drug Information Search Application

## เอกสารประกอบโปรเจกต์ฉบับภาษาไทย

---

## 🏗️ แหล่งที่มาของ Application

**Muler** เป็น Application ที่ Fork มาจาก [PizzaMyHeart/muler](https://github.com/PizzaMyHeart/muler) และได้รับการพัฒนาต่อเพิ่มเติม

- **Original Repository**: [PizzaMyHeart/muler](https://github.com/PizzaMyHeart/muler)
- **Original Discussion**: [Reddit - My first Python app](https://www.reddit.com/r/Python/comments/kbzkmv/my_first_python_app_a_simple_search_engine_for/)
- **Forked & Enhanced by**: Exzqqq (Current Repository)
- **ข้อมูลแหล่งที่มา**: [DrugBank Dataset](https://go.drugbank.com/releases/latest)
- **License**: CC BY-NC 4.0
- **Current Repository**: https://github.com/Exzqqq/muler

---

## 🔄 การปรับปรุงและพัฒนา

### การพัฒนาจาก Original Repository:

**Original Features (PizzaMyHeart/muler)**:

- Basic Flask web application
- SQLite database
- Simple drug search functionality
- Single language (English) support

### การปรับปรุงครั้งใหญ่ที่เพิ่มเติม:

1. **Database Migration**: จาก SQLite เป็น MySQL สำหรับ production
2. **Containerization**: แปลงเป็น Docker-based deployment
3. **Environment Management**: เพิ่ม environment variables และ .env configuration
4. **Multi-language Support**: รองรับภาษาไทยและอังกฤษ (ใหม่)
5. **Production Ready**: ปรับปรุงเพื่อใช้งานจริง
6. **Database Administration**: เพิ่ม phpMyAdmin interface
7. **Health Checks & Monitoring**: เพิ่ม container health monitoring

### การปรับปรุงเชิงเทคนิค:

- อัพเกรด Flask จาก 1.1.2 เป็น 2.3.3
- เพิ่ม cryptography package สำหรับ MySQL authentication
- ปรับปรุง database connection management
- เพิ่ม health checks และ restart policies
- เพิ่ม Docker Compose orchestration
- เพิ่ม persistent volume สำหรับ database
- ปรับปรุง security โดยใช้ environment variables

### ความแตกต่างจาก Original:

| Feature            | Original (PizzaMyHeart) | Enhanced (Exzqqq) |
| ------------------ | ----------------------- | ----------------- |
| Database           | SQLite                  | MySQL 8.0         |
| Deployment         | Manual                  | Docker Compose    |
| Languages          | English only            | Thai + English    |
| Admin Interface    | None                    | phpMyAdmin        |
| Environment Config | Hardcoded               | .env file         |
| Production Ready   | Development             | Production        |

---

## 🛠️ Tech Stack

### Backend:

- **Framework**: Flask 2.3.3 (Python Web Framework)
- **Database**: MySQL 8.0 (Production Database)
- **ORM**: SQLAlchemy (Database Abstraction)
- **Authentication**: cryptography>=3.4.8 (MySQL Security)

### Frontend:

- **Template Engine**: Jinja2 (Flask built-in)
- **Styling**: CSS3 + Custom Stylesheets
- **JavaScript**: Vanilla JS (Dynamic interactions)
- **Internationalization**: Flask-Babel (Multi-language support)

### Infrastructure:

- **Containerization**: Docker & Docker Compose
- **Database Admin**: phpMyAdmin (Web-based MySQL management)
- **Process Management**: Gunicorn (WSGI Server)
- **Networking**: Docker Bridge Network

### Dependencies:

```
Flask==2.3.3
Flask-Babel==4.0.0
PyMySQL==1.1.1
cryptography>=3.4.8
fuzzywuzzy==0.18.0
googletrans==4.0.0rc1
```

---

## 📱 Screenshots หน้าสำคัญของ Application

### 1. หน้าแรก (Home Page)

![Home Page](search.png)

- **ฟีเจอร์**: ช่องค้นหายาด้วยชื่อทางการหรือชื่อการค้า
- **การใช้งาน**: สามารถสลับภาษาไทย/อังกฤษได้
- **UI**: Clean และใช้งานง่าย

### 2. หน้าผลลัพธ์ (Results Page)

![Results Page](result.png)

- **ฟีเจอร์**: แสดงข้อมูลยาที่ค้นหา พร้อมรายละเอียดเภสัชวิทยา
- **การใช้งาน**: ข้อมูลครบถ้วนจาก DrugBank dataset
- **UI**: จัดระเบียบข้อมูลให้เข้าใจง่าย

---

## 🐳 Docker Images ที่ใช้

### 1. **mysql:8.0** (Official MySQL Image)

- **Purpose**: Production database server
- **Configuration**:
  - Character set: utf8mb4 (รองรับภาษาไทย)
  - Authentication: caching_sha2_password
  - Port: 3306
- **Volumes**: Persistent data storage
- **Health Check**: mysqladmin ping command

### 2. **phpmyadmin/phpmyadmin:latest** (Official phpMyAdmin)

- **Purpose**: Web-based database administration
- **Configuration**:
  - Connected to MySQL service
  - Port: 8081 (external)
- **Features**: Complete database management interface

### 3. **python:3.12-slim** (Custom Flask Application)

- **Base Image**: python:3.12-slim (Debian-based)
- **Build Type**: Single-stage build
- **System Dependencies**:
  ```dockerfile
  gcc
  default-libmysqlclient-dev
  pkg-config
  ```
- **Application Port**: 5000 (internal), 5001 (external)

---

## 🏗️ Build Process และ Base Image

### Single-Stage Build Strategy:

```dockerfile
FROM python:3.12-slim

# System dependencies installation
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config

# Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY . .
```

### เหตุผลที่เลือก Single-stage:

- **ความเรียบง่าย**: เหมาะสำหรับ Flask application
- **ขนาดเหมาะสม**: python:3.12-slim มีขนาดประหยัด
- **Development Friendly**: Easy debugging และ development

---

## 🔧 System Diagram

```mermaid
graph TB
    subgraph "Host System"
        Browser[Web Browser]
        Browser --> |"HTTP :5001"| FlaskApp
    end

    subgraph "Docker Network: muler_network"
        FlaskApp[Flask Application<br/>Container: muler_flask<br/>Port: 5000→5001]
        MySQL[MySQL Database<br/>Container: muler_mysql<br/>Port: 3306]
        PHPMyAdmin[phpMyAdmin<br/>Container: muler_phpmyadmin<br/>Port: 80→8081]

        FlaskApp --> |"mysql://mysql:3306"| MySQL
        PHPMyAdmin --> |"mysql://mysql:3306"| MySQL
    end

    subgraph "Volumes"
        MySQLData[mysql_data<br/>Persistent Storage]
        MySQL --> MySQLData
    end

    subgraph "External Access"
        AdminPanel[Database Admin<br/>localhost:8081]
        MainApp[Main Application<br/>localhost:5001]
    end

    Browser --> |"Access"| MainApp
    Browser --> |"Admin"| AdminPanel
```

### Port Mapping:

- **Flask Application**: `5001:5000` (External:Internal)
- **MySQL Database**: `3306:3306` (External:Internal)
- **phpMyAdmin**: `8081:80` (External:Internal)

### Network Configuration:

- **Network Type**: Bridge Network
- **Network Name**: `muler_network`
- **Inter-container Communication**: Service name resolution
- **Security**: Isolated from host network

---

## 📄 Docker Compose Configuration

### ไฟล์ docker-compose.yml:

```yaml
version: "3.8"

services:
  # MySQL Database Service
  mysql:
    image: mysql:8.0
    container_name: muler_mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./muler/database/muler.sql:/docker-entrypoint-initdb.d/muler.sql:ro
    networks:
      - muler_network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 20s
      retries: 10

  # Database Administration
  phpmyadmin:
    image: phpmyadmin/phpmyadmin:latest
    container_name: muler_phpmyadmin
    restart: unless-stopped
    environment:
      PMA_HOST: mysql
      PMA_PORT: ${MYSQL_PORT}
      PMA_USER: ${MYSQL_USER}
      PMA_PASSWORD: ${MYSQL_PASSWORD}
    ports:
      - "${PHPMYADMIN_PORT}:80"
    depends_on:
      mysql:
        condition: service_healthy
    networks:
      - muler_network

  # Flask Application
  flask_app:
    build: .
    container_name: muler_flask
    restart: unless-stopped
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@mysql:${MYSQL_PORT}/${MYSQL_DATABASE}
    ports:
      - "${FLASK_PORT}:5000"
    depends_on:
      mysql:
        condition: service_healthy
    networks:
      - muler_network
    volumes:
      - .:/app

volumes:
  mysql_data:

networks:
  muler_network:
    driver: bridge
```

### Environment Variables (.env):

```env
# Database Configuration
MYSQL_ROOT_PASSWORD=muler_root_password
MYSQL_DATABASE=muler
MYSQL_USER=muler_user
MYSQL_PASSWORD=muler_password
MYSQL_PORT=3306

# Application Ports
FLASK_PORT=5001
PHPMYADMIN_PORT=8081

# Flask Configuration
FLASK_ENV=production
```

---

## 🚀 การติดตั้งและใช้งาน

### 1. เตรียม Environment:

```bash
cp .env.example .env
# แก้ไขค่าต่างๆ ใน .env file
```

### 2. เริ่มใช้งาน:

```bash
docker compose up -d
```

### 3. เข้าถึง Services:

- **Main Application**: http://localhost:5001
- **Database Admin**: http://localhost:8081
- **Database Direct**: mysql://localhost:3306

### 4. หยุดการทำงาน:

```bash
docker compose down
```

---

## 📊 คุณสมบัติเด่น

1. **Multi-language Support**: ภาษาไทย/อังกฤษ
2. **Drug Search**: ค้นหาด้วยชื่อยาทางการหรือชื่อการค้า
3. **Comprehensive Data**: ข้อมูลเภสัชวิทยาครบถ้วนจาก DrugBank
4. **Production Ready**: Docker containerization
5. **Easy Deployment**: One-command deployment
6. **Database Management**: Web-based admin interface
7. **Persistent Data**: Volume-based data storage

---

_เอกสารนี้จัดทำขึ้นเพื่อประกอบการนำเสนอโปรเจกต์ Muler Drug Information Search Application_
