# Database Final Project
This is the repo holds source code for the final project of Databases CSCI-SHU 213 2020 Fall
## Roadmap

- [x]  1. `Register` (Customer, Booking agent, Airline staff)
- [x]  2. `Login` (Customer, Booking agent, Airline staff)
- [x]  3. `Logout` (Customer, Booking agent, Airline staff)
- [x]  4. `View my flights` (Customer, Booking agent, Airline staff)
- [x]  5. `Search for flights` (Customer, Booking agent)
- [x]  6. `Purchase tickets` (Customer, Booking agent)
- [x]  7. `Track my spending` (Customer, Booking agent)
- [x]  8. `View my commission` (Booking agent)
- [x]  9. `View top customers` (Booking agent)
- [x]  10. `View public info` (Anyone)
- [x]  11. `Create new flights` (Airline staff)
- [x]  12. `Change Status of flights` (Airline staff)
- [x]  13. `Add airplane in the system` (Airline staff)
- [x]  14. `Add new airport in the system` (Airline staff)
- [x]  15. `View all the booking agents` (Airline staff)
- [x]  16. `View frequent customers` (Airline staff)
- [x]  17. `View reports` (Airline staff)
- [x]  18. `Comparison of revenue earned` (Airline staff)
- [x]  19. `View Top destinations` (Airline staff)


## Use Cases
  1. Public search
    ![Public search Page](https://github.com/BoyanXu/database-final-project/blob/main/static/img/public%20search%20page.png?raw=true)
  2. Customer Homepage
    ![Customer Homepage1](https://github.com//BoyanXu/database-final-project/blob/main/static/img/customer%20homepage1.png?raw=true)
    ![Customer Homepage2](https://github.com//BoyanXu/database-final-project/blob/main/static/img/customer%20homepage2.png?raw=true)
  3. Customer Search Flight
  ![Customer Search Flight](https://github.com//BoyanXu/database-final-project/blob/main/static/img/customer%20search%20flight.png?raw=true)
  4. Customer Purchase Ticket
  ![Customer Purchase Ticket](https://github.com//BoyanXu/database-final-project/blob/main/static/img/customer%20purchase%20ticket.png?raw=true)

  5. Agent Homepage
  ![Agent Homepage](https://github.com//BoyanXu/database-final-project/blob/main/static/img/agent%20homepage.png?raw=true)

  6. Agent Search Flight
  ![Agent Search Flight](https://github.com//BoyanXu/database-final-project/blob/main/static/img/agent%20search.png?raw=true)

  7. Agent Purchase Ticket
  ![Agent Purchase Ticket](https://github.com//BoyanXu/database-final-project/blob/main/static/img/agent%20purchase.png?raw=true)

  8. Agent View Customer
  ![Agent View Customer](https://github.com//BoyanXu/database-final-project/blob/main/static/img/agent%20view%20top%20customer.png?raw=true)

  9. Staff Homepage
  ![Staff Homepage](https://github.com//BoyanXu/database-final-project/blob/main/static/img/staff%20homepage1.png?raw=true)
  ![Staff Homepage](https://github.com//BoyanXu/database-final-project/blob/main/static/img/staff%20homepage2.png?raw=true)
  ![Staff Homepage](https://github.com//BoyanXu/database-final-project/blob/main/static/img/staff%20homepage3.png?raw=true)

  10. Staff Create Flight
  ![Staff Create Flight](https://github.com//BoyanXu/database-final-project/blob/main/static/img/staff%20create%20flight.png?raw=true)

  11. Staff Create Airplane
  ![Staff Create Airplane](https://github.com//BoyanXu/database-final-project/blob/main/static/img/staff%20create%20airplane.png?raw=true)

  12. Staff Create Airport
  ![Staff Create Airport](https://github.com//BoyanXu/database-final-project/blob/main/static/img/staff%20create%20airport.png?raw=true)

  13. Staff View Agent
  ![Staff View Agent](https://github.com//BoyanXu/database-final-project/blob/main/static/img/staff%20view%20agent.png?raw=true)

  14. Staff View Report
  ![Staff View Report](https://github.com//BoyanXu/database-final-project/blob/main/static/img/staff%20view%20report.png?raw=true)
## Project Structure


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
        ├── agentPurchase.html
        ├── agentViewCustomer.html
        ├── customerHome.html
        ├── customerPurchase.html
        ├── customerSearch.html
        ├── placeholder.about.html
        ├── placeholder.home.html
        ├── publicSearch.html
        ├── staffCreateAirplane.html
        ├── staffCreateAirport.html
        ├── staffCreateFlight.html
        ├── staffHome.html
        ├── staffViewAgent.html
        └── staffViewReport.html
  ```

## Accuse for Flight_Search demo failure


Unnecessary filter condition for arrival time.
```sql
AND '2020-12-21' BETWEEN DATE_SUB(f.arrival_time, INTERVAL 2 DAY) AND DATE_ADD(f.arrival_time, INTERVAL 2 DAY)

```