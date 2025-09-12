# Container Architecture & ERD Diagram

## 🏗️ Container Relationship Diagram

```mermaid
graph TB
    subgraph "Docker Network: muler_network"
        subgraph "Application Layer"
            Flask[muler_flask<br/>📱 Flask App<br/>Port: 5001]
            PHP[muler_phpmyadmin<br/>🖥️ phpMyAdmin<br/>Port: 8080]
        end
        
        subgraph "Data Layer"
            MySQL[muler_mysql<br/>🗄️ MySQL 8.0<br/>Port: 3306]
        end
        
        subgraph "External Access"
            User[👤 End Users]
            Admin[👨‍💼 DB Admin]
        end
    end
    
    %% Connections
    Flask -->|"DATABASE_URL<br/>mysql+pymysql://"| MySQL
    PHP -->|"PMA_HOST: mysql<br/>MySQL Protocol"| MySQL
    
    User -->|"http://localhost:5001<br/>Web Interface"| Flask
    Admin -->|"http://localhost:8080<br/>DB Management"| PHP
    
    %% Styling
    classDef container fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef database fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef user fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    
    class Flask,PHP container
    class MySQL database
    class User,Admin user
```

## 🔄 Data Flow Architecture

```mermaid
sequenceDiagram
    participant U as User
    participant F as muler_flask
    participant M as muler_mysql
    participant A as Admin
    participant P as muler_phpmyadmin
    
    Note over F,M: Application Data Flow
    U->>F: Search for drug
    F->>M: SQL Query
    M->>F: Drug data
    F->>U: Search results
    
    Note over P,M: Database Management Flow
    A->>P: Access phpMyAdmin
    P->>M: Admin queries
    M->>P: Database info
    P->>A: Management interface
    
    Note over F,P: Independent Services
    Note right of F: Flask handles<br/>user requests
    Note right of P: phpMyAdmin handles<br/>DB administration
```

## 🏷️ Database Entity Relationship

```mermaid
erDiagram
    DRUG_INFO {
        int id PK
        string drug_name
        string description
        string category
        text details
    }
    
    DRUG_NAMES {
        int id PK
        int drug_id FK
        string name_type
        string name_value
    }
    
    DRUG_INTERACTIONS {
        int id PK
        int drug1_id FK
        int drug2_id FK
        string interaction_type
        string severity
    }
    
    DRUG_INFO ||--o{ DRUG_NAMES : "has multiple names"
    DRUG_INFO ||--o{ DRUG_INTERACTIONS : "participates in"
```

## 📋 Connection Details

### Flask → MySQL Connection
```yaml
DATABASE_URL: mysql+pymysql://user:password@mysql:3306/muler_db
```

### phpMyAdmin → MySQL Connection  
```yaml
PMA_HOST: mysql
PMA_PORT: 3306
PMA_USER: ${MYSQL_USER}
PMA_PASSWORD: ${MYSQL_PASSWORD}
```

## 🎯 Key Points

1. **Flask & phpMyAdmin are PARALLEL services**
   - Both connect to same MySQL database
   - Serve different purposes
   - No direct communication between them

2. **phpMyAdmin Role**
   - Database administration tool
   - Visual interface for MySQL
   - Allows direct SQL queries
   - NOT part of application logic

3. **Network Architecture**
   - All containers in same Docker network
   - MySQL accessible by hostname "mysql"
   - Isolated from external networks
   - Port mapping for external access

4. **Data Flow**
   - **Users** → Flask → MySQL (application data)
   - **Admins** → phpMyAdmin → MySQL (database management)
   - **Independent flows** - no cross-contamination
