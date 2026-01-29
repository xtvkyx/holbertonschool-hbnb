# HBnB Database ER Diagram (Mermaid)

```mermaid
erDiagram
    USERS {
        string id PK
        string email "UNIQUE, NOT NULL"
        string password_hash "NOT NULL"
        boolean is_admin "NOT NULL, DEFAULT false"
    }

    PLACES {
        string id PK
        string title "NOT NULL"
        string description "NULL"
        float price "NOT NULL, DEFAULT 0.0"
        float latitude "NULL"
        float longitude "NULL"
        string owner_id FK "NOT NULL -> USERS.id"
    }

    REVIEWS {
        string id PK
        string text "NOT NULL"
        int rating "NULL"
        string user_id FK "NOT NULL -> USERS.id"
        string place_id FK "NOT NULL -> PLACES.id"
    }

    AMENITIES {
        string id PK
        string name "UNIQUE, NOT NULL"
    }

    PLACE_AMENITY {
        string place_id PK, FK "-> PLACES.id"
        string amenity_id PK, FK "-> AMENITIES.id"
    }

    %% Relationships
    USERS ||--o{ PLACES : "owns"
    USERS ||--o{ REVIEWS : "writes"
    PLACES ||--o{ REVIEWS : "has"

    %% Many-to-Many via association table
    PLACES ||--o{ PLACE_AMENITY : "links"
    AMENITIES ||--o{ PLACE_AMENITY : "links"
