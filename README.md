# Database Final Project
This is the repo holds source code for the final project of Databases CSCI-SHU 213 2020 Fall
## Roadmap
---
- [ ]  1. `Register` (Customer, Booking agent, Airline staff)
- [x]  2. `Login` (Customer, Booking agent, Airline staff)
- [x]  3. `Logout` (Customer, Booking agent, Airline staff)
- [x]  4. `View my flights` (Customer, Booking agent, Airline staff)
- [x]  5. `Search for flights` (Customer, Booking agent)
- [x]  6. `Purchase tickets` (Customer, Booking agent)
- [ ]  7. `Track my spending` (Customer, Booking agent)
- [x]  8. `View my commission` (Booking agent)
- [ ]  9. `View top customers` (Booking agent)
- [x]  10. `View public info` (Anyone)
- [x]  11. `Create new flights` (Airline staff)
- [x]  12. `Change Status of flights` (Airline staff)
- [x]  13. `Add airplane in the system` (Airline staff)
- [x]  14. `Add new airport in the system` (Airline staff)
- [x]  15. `View all the booking agents` (Airline staff)
- [ ]  16. `View frequent customers` (Airline staff)
- [ ]  17. `View reports` (Airline staff)
- [ ]  18. `Comparison of revenue earned` (Airline staff)
- [ ]  19. `View Top destinations` (Airline staff)


Project Structure
--------

  ```sh
├── README.md
├── agent.py
├── app.py
├── appconf.py
├── config.py
├── customer.py
├── docs
│   ├── create_database.sql
│   ├── database_model.png
│   ├── insert_init_records.sql
│   └── test_query_data.sql
├── forms.py
├── login.py
├── models.py
├── register.py
├── requirements.txt
├── staff.py
└── templates
    ├── errors
    │   ├── 404.html
    │   └── 500.html
    ├── forms
    │   ├── forgot.html
    │   ├── login.html
    │   ├── register.html
    │   ├── registerAgent.html
    │   ├── registerCustomer.html
    │   └── registerStaff.html
    ├── layouts
    │   ├── form.html
    │   └── main.html
    └── pages
        ├── agentHome.html
        ├── customerHome.html
        ├── customerPurchase.html
        ├── customerSearch.html
        ├── placeholder.about.html
        ├── placeholder.home.html
        ├── publicSearch.html
        ├── staffCreateAirplane.html
        ├── staffCreateAirport.html
        ├── staffCreateFlight.html
        └── staffHome.html
  ```