# holbertonschool-hbnb
# HBnB Evolution Project: Part 1 🏠

Welcome to the **HBnB Evolution Project**!  
This project is a backend-focused web application inspired by AirBnB, developed as part of the Holberton School curriculum. In Part 1, we focus on **system design, architecture, and documentation** to establish a strong foundation before implementation.

---

## Project Overview 🌟

HBnB Evolution aims to model a platform where users can list places for rent, submit reviews, and browse available accommodations.  
This first phase emphasizes **planning and design**, ensuring that the system is well-structured, scalable, and easy to maintain.

Rather than writing production code immediately, Part 1 concentrates on understanding how the system should behave and how its components interact.

---

## What’s Included in Part 1? 🧩

### UML-Based System Design
Unified Modeling Language (UML) is used to visually represent the system structure and behavior. These diagrams act as a blueprint for future development and help clarify responsibilities across the system.

The UML documentation includes:
- A high-level architectural overview
- Detailed business logic modeling
- Sequence diagrams for core API interactions

---

## System Architecture 🏗️

The HBnB application follows a **three-layer architecture**, promoting separation of concerns and modularity.

### Presentation Layer (Services / API)
This layer handles user interaction with the system. It receives API requests, validates input, manages authentication, and returns appropriate responses to clients.

### Business Logic Layer (Models)
This layer contains the core domain entities and business rules. It defines how users, places, reviews, and amenities behave and interact with one another.

### Persistence Layer
The persistence layer is responsible for storing and retrieving data. In early stages, data may be file-based, with future plans to migrate to a database-backed solution for scalability.

### Facade Pattern
A **Facade** is used as a single entry point between the Presentation Layer and the rest of the system. This simplifies communication, reduces coupling, and centralizes business operations.

---

## Core Data Models 🧱

### User
Represents a system user. Users can register, update their profile, own places, and write reviews.

### Place
Represents a rental listing. A place is owned by a user, may include multiple amenities, and can receive reviews.

### Review
Represents user feedback for a place. Each review is written by one user and is associated with one place.

### Amenity
Represents a feature or service (e.g., Wi-Fi, parking). Amenities can be shared across multiple places.

All entities share common attributes such as a unique identifier and timestamps for creation and updates.

---

## Business Rules 📏

- Each entity has a **unique UUID4 identifier**
- A user can own multiple places
- A place has exactly one owner
- Users may write reviews for places they do not own
- Places can include multiple amenities
- Amenities can be reused across different places
- Each review belongs to exactly one user and one place

---

## API Interaction Flow 🔄

To better understand system behavior, sequence diagrams illustrate how requests move through the layers.

### User Registration
A user submits registration data through the API. The request is validated, processed by the business logic, stored in persistence, and a confirmation response is returned.

### Place Creation
An authenticated user submits place details. The system validates ownership rules, creates the place entity, and saves it.

### Review Submission
A user submits a review for a place. The system verifies the user and place, saves the review, and confirms the operation.

### Fetching Places
Users can request a list of places with optional filters. The system processes the filters and retrieves matching places from storage.

---

## Why This Design Matters 💡

- **Scalability:** Clear separation allows easy expansion
- **Maintainability:** Each layer has a single responsibility
- **Clarity:** UML diagrams reduce ambiguity
- **Testability:** Business logic can be tested independently
- **Consistency:** Shared base attributes ensure uniformity

---

## Documentation Goal 📘

This documentation serves as:
- A reference for developers
- A guide for implementation
- A validation of system design decisions

It ensures that development in later phases follows a clear and consistent plan.

---

## Team 👥

**Members:**
- Raneem Alsaqat
- Amjaad Alomani
- Lamis Aljabli  

Our team collaborates closely to design, document, and validate the HBnB system architecture.

---

## Status 🚀

- ✅ Architecture defined  
- ✅ UML diagrams completed  
- ✅ Business rules documented  
- ⏳ Implementation coming in next phases  

---

## License 📄

This project is developed for educational purposes as part of the Holberton School curriculum.
