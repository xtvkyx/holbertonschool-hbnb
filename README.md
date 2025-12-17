## High-Level Package Diagram

```mermaid
classDiagram
direction LR

namespace "Presentation Layer\n(Services / API)" as PL {
  class API {
    <<package>>
    +REST Endpoints
    +Controllers/Routes
  }

  class Services {
    <<package>>
    +Request validation
    +Auth handlers
  }
}

namespace "Facade\n(Application Interface)" as FAC {
  class HBnBFacade {
    <<facade>>
    +create_user()
    +create_place()
    +create_review()
    +list_places()
  }
}

namespace "Business Logic Layer\n(Models)" as BL {
  class Models {
    <<package>>
    +User
    +Place
    +Review
    +Amenity
  }
}

namespace "Persistence Layer" as PERS {
  class Repositories {
    <<package>>
    +UserRepository
    +PlaceRepository
    +ReviewRepository
    +AmenityRepository
  }

  class Database {
    <<database>>
  }
}

API --> HBnBFacade : calls
Services --> HBnBFacade : uses
HBnBFacade --> Models : business rules
HBnBFacade --> Repositories : CRUD
Repositories --> Database : queries

```markdown
## Explanatory Notes

### Presentation Layer
- Handles user interaction through REST APIs and services.
- Validates requests and formats responses.
- Does **not** contain business logic.

### Business Logic Layer
- Contains core domain models such as User, Place, Review, and Amenity.
- Applies business rules and validations.
- Independent from HTTP and database details.

### Persistence Layer
- Responsible for storing and retrieving data.
- Uses repositories or DAOs to interact with the database.
- Isolated from business and presentation concerns.

### Facade Pattern Usage
- The `HBnBFacade` acts as a single entry point to the application logic.
- The Presentation layer communicates only with the facade.
- The facade coordinates business logic and persistence operations.
- This reduces coupling and improves maintainability.
