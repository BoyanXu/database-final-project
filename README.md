# Database Final Project
This is the repo holds source code for the final project of Databases CSCI-SHU 213 2020 Fall

## Team
- Team Member: Boyan & Weiran

- Boyan works on:
  1. `View public info` (Anyone)
  2. `Create new flights` (Airline staff)
  3. `Change Status of flights` (Airline staff)
  4. `Add airplane in the system` (Airline staff)
  5. `Add new airport in the system` (Airline staff)
  6. `View all the booking agents` (Airline staff)
  7. `View frequent customers` (Airline staff)
  8. `View reports` (Airline staff)
  9. `Comparison of revenue earned` (Airline staff)
  10. `View Top destinations` (Airline staff)

- Weiran works on:
  1. `Register` (Customer, Booking agent, Airline staff)
  2. `Login` (Customer, Booking agent, Airline staff)
  3. `Logout` (Customer, Booking agent, Airline staff)
  4. `View my flights` (Customer, Booking agent, Airline staff)
  5. `Search for flights` (Customer, Booking agent)
  6. `Purchase tickets` (Customer, Booking agent)
  7. `Track my spending` (Customer, Booking agent)
  8. `View my commission` (Booking agent)
  9. `View top customers` (Booking agent)


## Use case
The sql queries executed by a use case are documented in [test\_query\_data.sql](docs/test_query_data.sql)
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

## Setup
1. Create virtual environment:
    ```sh
    virtualenv --no-site-packages env
    ```
2. Install required packages:
    ```sh
    pip install -r requirement.txt
    ```
3. Initialize database:
   1. Download & install XAMPP 7.2.33 (Version matter!)
   2. Start MySQL server & go to http://localhost/phpmyadmin/
   3. Create an account named "root" and choose "No password" and "Unix Socket based authentication"
   4. Depend on your system, go to [appconf.py](appconf.py) and set path to unix_socket correctly
   5. Run [create\_database.sql](docs/create_database.sql) to create the database `airline_service_db`
   6. Run [insert\_init\_records.sql](docs/insert_init_records.sql) to insert test data into the db
4. Run flask app & go to homepage:
    ```sh
    python app.py
    ```
## File structure
- 📂 __database\-final\-project__
   - 📄 [README.md](README.md) <- Document for setup the project locally
   - 📄 [agent.py](agent.py)  <- Agent request handlers
   - 📄 [app.py](app.py)    <- Entrance program
   - 📄 [appconf.py](appconf.py) <- Connect to MySQL server, default user is `root` with no password
   - 📄 [config.py](config.py)  <- Flask Config file
   - 📄 [customer.py](customer.py)  <- Customer request handlers
   - 📂 __docs__
     - 📄 [create\_database.sql](docs/create_database.sql)  <- Setup database
     - 📄 [database\_model.png](docs/database_model.png)    <- Database schema diagram
     - 📄 [insert\_init\_records.sql](docs/insert_init_records.sql)  <- Insert initial data
     - 📄 [test\_query\_data.sql](docs/test_query_data.sql)  <- List testing intermediate queries
   - 📄 [forms.py](forms.py)  <- Declare flaskWTForm
   - 📄 [login.py](login.py)  <- Login request handlers
   - 📄 [register.py](register.py)  <- Register request handlers
   - 📄 [requirements.txt](requirements.txt)  <- Python libraries to install
   - 📄 [staff.py](staff.py)  <- Staff request handlers
   - 📂 __static__  <- Static resources
     - ...
   - 📂 __templates__
     - 📂 __errors__
       - 📄 [404.html](templates/errors/404.html)  <- 404 page
       - 📄 [500.html](templates/errors/500.html)  <- 500 page
     - 📂 __forms__
       - 📄 [login.html](templates/forms/login.html)  <- Login page
       - 📄 [register.html](templates/forms/register.html)  <- Register page
       - 📄 [registerAgent.html](templates/forms/registerAgent.html)  <- Register agent page
       - 📄 [registerCustomer.html](templates/forms/registerCustomer.html)  <- Register customer page
       - 📄 [registerStaff.html](templates/forms/registerStaff.html)  <- Register staff page
     - 📂 __layouts__
       - 📄 [form.html](templates/layouts/form.html)  <- form layout template
       - 📄 [main.html](templates/layouts/main.html)  <- main layout template
     - 📂 __pages__
       - 📄 [agentHome.html](templates/pages/agentHome.html)  <- Agent homepage
       - 📄 [agentPurchase.html](templates/pages/agentPurchase.html)  <- Agent purchase page
       - 📄 [agentSearch.html](templates/pages/agentSearch.html)  <- Agent search page
       - 📄 [agentViewCustomer.html](templates/pages/agentViewCustomer.html)  <- Agent view customer page
       - 📄 [customerHome.html](templates/pages/customerHome.html)  <- Customer homepage
       - 📄 [customerPurchase.html](templates/pages/customerPurchase.html)  <- Customer purchase page
       - 📄 [customerSearch.html](templates/pages/customerSearch.html)  <- Customer search page
       - 📄 [placeholder.about.html](templates/pages/placeholder.about.html)  <- placeholder about page
       - 📄 [placeholder.home.html](templates/pages/placeholder.home.html)  <- placeholder home page
       - 📄 [publicSearch.html](templates/pages/publicSearch.html)  <- Public search page
       - 📄 [staffCheckCustomer.html](templates/pages/staffCheckCustomer.html)  <- Staff check customer page
       - 📄 [staffCreateAirplane.html](templates/pages/staffCreateAirplane.html)  <- Staff create airplane page
       - 📄 [staffCreateAirport.html](templates/pages/staffCreateAirport.html)  <- Staff create airport page
       - 📄 [staffCreateFlight.html](templates/pages/staffCreateFlight.html)  <- Staff create flight page
       - 📄 [staffHome.html](templates/pages/staffHome.html)  <- Staff homepage
       - 📄 [staffViewAgent.html](templates/pages/staffViewAgent.html)  <- Staff view agent page
       - 📄 [staffViewReport.html](templates/pages/staffViewReport.html)  <- Staff view report page


## Use case demo
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

## PS: Accuse for Flight_Search demo failure


Unnecessary filter condition for arrival time.
```sql
AND '2020-12-21' BETWEEN DATE_SUB(f.arrival_time, INTERVAL 2 DAY) AND DATE_ADD(f.arrival_time, INTERVAL 2 DAY)

```