# SphereBnB

A modern property rental and accommodation booking platform built using Django and Django REST Framework.

> **Project Status:** Work in Progress (WIP)

## Overview

SphereBnB is a backend-focused accommodation booking platform inspired by Airbnb. The project is designed to provide a robust and scalable backend architecture for property listing, booking management, user authentication, and host-guest interactions.

The primary goal of this project is to strengthen backend development skills while implementing real-world software engineering concepts such as authentication, database design, REST APIs, permissions, and deployment workflows.

---

## Features

### User Management

* User Registration
* User Login & Authentication
* Profile Management
* Role-Based Access Control

### Property Management

* Create Property Listings
* Update Property Details
* Delete Property Listings
* Browse Available Properties

### Booking System

* Create Bookings
* View Booking History
* Booking Status Tracking

### Search & Discovery

* Browse Listings
* View Property Details
* Search and Filter Support

### API Support

* RESTful API Architecture
* Serializer-Based Validation
* Authentication & Permissions

---

## Tech Stack

### Backend

* Python
* Django
* Django REST Framework

### Database

* SQLite (Development)
* PostgreSQL (Planned for Production)

### Version Control

* Git
* GitHub

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/SphereBnB.git
cd SphereBnB
```

### Create a Virtual Environment

```bash
python3 -m venv venv
```

### Activate the Virtual Environment

#### Linux / macOS

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create a Superuser

```bash
python manage.py createsuperuser
```

### Run the Development Server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

---

## Project Structure

```text
SphereBnB/
│
├── accounts/
├── listings/
├── bookings/
├── core/
├── media/
├── static/
├── templates/
├── manage.py
├── requirements.txt
└── README.md
```

---

## Sample API Endpoints

```text
/api/auth/register/
/api/auth/login/
/api/profile/
/api/properties/
/api/properties/<id>/
/api/bookings/
```

---

## Future Enhancements

* JWT Authentication
* Property Reviews & Ratings
* Wishlist Functionality
* Payment Gateway Integration
* Email Notifications
* Property Availability Calendar
* Docker Support
* AWS Deployment
* Recommendation Engine
* Advanced Search Filters

---

## Learning Objectives

This project focuses on:

* Django Fundamentals
* Django REST Framework
* Authentication & Authorization
* Database Design
* API Development
* Backend Architecture
* Deployment Workflows
* Git & GitHub Collaboration

---

## Contributing

Contributions, bug reports, and feature suggestions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

## License

This project is built for educational, learning, and portfolio purposes.

---

## Author

**Ayush Srivastava**

Backend Developer | Django | DRF | AWS | Web3
