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
