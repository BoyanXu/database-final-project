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

## File Structure
- 📂 __flask\-boilerplate__
   - 📄 [README.md](README.md)
   - 📄 [agent.py](agent.py)
   - 📄 [app.py](app.py)
   - 📄 [appconf.py](appconf.py)
   - 📄 [config.py](config.py)
   - 📄 [customer.py](customer.py)
   - 📂 __docs__
     - 📄 [create\_database.sql](docs/create_database.sql)
     - 📄 [database\_model.png](docs/database_model.png)
     - 📄 [insert\_init\_records.sql](docs/insert_init_records.sql)
     - 📄 [test\_query\_data.sql](docs/test_query_data.sql)
   - 📄 [forms.py](forms.py)
   - 📄 [login.py](login.py)
   - 📄 [models.py](models.py)
   - 📄 [register.py](register.py)
   - 📄 [requirements.txt](requirements.txt)
   - 📄 [staff.py](staff.py)
   - 📂 __static__
     - 📂 __css__
       - 📄 [bootstrap\-3.1.1.min.css](static/css/bootstrap-3.1.1.min.css)
       - 📄 [bootstrap\-theme\-3.1.1.css](static/css/bootstrap-theme-3.1.1.css)
       - 📄 [bootstrap\-theme\-3.1.1.min.css](static/css/bootstrap-theme-3.1.1.min.css)
       - 📄 [bootstrap\-theme.css.map](static/css/bootstrap-theme.css.map)
       - 📄 [bootstrap.css.map](static/css/bootstrap.css.map)
       - 📄 [font\-awesome\-4.1.0.min.css](static/css/font-awesome-4.1.0.min.css)
       - 📄 [layout.forms.css](static/css/layout.forms.css)
       - 📄 [layout.main.css](static/css/layout.main.css)
       - 📄 [main.css](static/css/main.css)
       - 📄 [main.quickfix.css](static/css/main.quickfix.css)
       - 📄 [main.responsive.css](static/css/main.responsive.css)
     - 📂 __fonts__
       - 📄 [FontAwesome.otf](static/fonts/FontAwesome.otf)
       - 📄 [fontawesome\-webfont.eot](static/fonts/fontawesome-webfont.eot)
       - 📄 [fontawesome\-webfont.svg](static/fonts/fontawesome-webfont.svg)
       - 📄 [fontawesome\-webfont.ttf](static/fonts/fontawesome-webfont.ttf)
       - 📄 [fontawesome\-webfont.woff](static/fonts/fontawesome-webfont.woff)
     - 📂 __ico__
       - 📄 [apple\-touch\-icon\-114\-precomposed.png](static/ico/apple-touch-icon-114-precomposed.png)
       - 📄 [apple\-touch\-icon\-144\-precomposed.png](static/ico/apple-touch-icon-144-precomposed.png)
       - 📄 [apple\-touch\-icon\-57\-precomposed.png](static/ico/apple-touch-icon-57-precomposed.png)
       - 📄 [apple\-touch\-icon\-72\-precomposed.png](static/ico/apple-touch-icon-72-precomposed.png)
       - 📄 [favicon.png](static/ico/favicon.png)
     - 📂 __img__
       - 📄 [agent homepage.png](static/img/agent%20homepage.png)
       - 📄 [agent purchase.png](static/img/agent%20purchase.png)
       - 📄 [agent search.png](static/img/agent%20search.png)
       - 📄 [agent view top customer.png](static/img/agent%20view%20top%20customer.png)
       - 📄 [customer homepage1.png](static/img/customer%20homepage1.png)
       - 📄 [customer homepage2.png](static/img/customer%20homepage2.png)
       - 📄 [customer purchase ticket.png](static/img/customer%20purchase%20ticket.png)
       - 📄 [customer search flight.png](static/img/customer%20search%20flight.png)
       - 📄 [public search page.png](static/img/public%20search%20page.png)
       - 📄 [staff create airplane.png](static/img/staff%20create%20airplane.png)
       - 📄 [staff create airport.png](static/img/staff%20create%20airport.png)
       - 📄 [staff create flight.png](static/img/staff%20create%20flight.png)
       - 📄 [staff homepage1.png](static/img/staff%20homepage1.png)
       - 📄 [staff homepage2.png](static/img/staff%20homepage2.png)
       - 📄 [staff homepage3.png](static/img/staff%20homepage3.png)
       - 📄 [staff view agent.png](static/img/staff%20view%20agent.png)
       - 📄 [staff view report.png](static/img/staff%20view%20report.png)
     - 📂 __js__
       - 📂 __libs__
         - 📄 [bootstrap\-3.1.1.min.js](static/js/libs/bootstrap-3.1.1.min.js)
         - 📄 [jquery\-1.11.1.min.js](static/js/libs/jquery-1.11.1.min.js)
         - 📄 [jquery\-1.11.1.min.map](static/js/libs/jquery-1.11.1.min.map)
         - 📄 [modernizr\-2.8.2.min.js](static/js/libs/modernizr-2.8.2.min.js)
         - 📄 [respond\-1.4.2.min.js](static/js/libs/respond-1.4.2.min.js)
       - 📄 [plugins.js](static/js/plugins.js)
       - 📄 [script.js](static/js/script.js)
   - 📂 __templates__
     - 📂 __errors__
       - 📄 [404.html](templates/errors/404.html)
       - 📄 [500.html](templates/errors/500.html)
     - 📂 __forms__
       - 📄 [forgot.html](templates/forms/forgot.html)
       - 📄 [login.html](templates/forms/login.html)
       - 📄 [register.html](templates/forms/register.html)
       - 📄 [registerAgent.html](templates/forms/registerAgent.html)
       - 📄 [registerCustomer.html](templates/forms/registerCustomer.html)
       - 📄 [registerStaff.html](templates/forms/registerStaff.html)
     - 📂 __layouts__
       - 📄 [form.html](templates/layouts/form.html)
       - 📄 [main.html](templates/layouts/main.html)
     - 📂 __pages__
       - 📄 [agentHome.html](templates/pages/agentHome.html)
       - 📄 [agentPurchase.html](templates/pages/agentPurchase.html)
       - 📄 [agentSearch.html](templates/pages/agentSearch.html)
       - 📄 [agentViewCustomer.html](templates/pages/agentViewCustomer.html)
       - 📄 [customerHome.html](templates/pages/customerHome.html)
       - 📄 [customerPurchase.html](templates/pages/customerPurchase.html)
       - 📄 [customerSearch.html](templates/pages/customerSearch.html)
       - 📄 [placeholder.about.html](templates/pages/placeholder.about.html)
       - 📄 [placeholder.home.html](templates/pages/placeholder.home.html)
       - 📄 [publicSearch.html](templates/pages/publicSearch.html)
       - 📄 [staffCheckCustomer.html](templates/pages/staffCheckCustomer.html)
       - 📄 [staffCreateAirplane.html](templates/pages/staffCreateAirplane.html)
       - 📄 [staffCreateAirport.html](templates/pages/staffCreateAirport.html)
       - 📄 [staffCreateFlight.html](templates/pages/staffCreateFlight.html)
       - 📄 [staffHome.html](templates/pages/staffHome.html)
       - 📄 [staffViewAgent.html](templates/pages/staffViewAgent.html)
       - 📄 [staffViewReport.html](templates/pages/staffViewReport.html)


## Use Case Demo
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