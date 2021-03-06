------------------------------------------------------------------
-- Customer
  -- Homepage
  SELECT purchases.ticket_id,
    ticket.airline_name,
    ticket.flight_num,
    flight.departure_airport,
    flight.departure_time,
    flight.arrival_airport,
    flight.arrival_time,
    flight.price,
    flight.status,
    flight.airplane_id
    FROM purchases, ticket, flight
        WHERE purchases.customer_email = 'one@nyu.edu'
          AND purchases.ticket_id = ticket.ticket_id
          AND ticket.airline_name = flight.airline_name
          AND ticket.flight_num = flight.flight_num
          AND departure_time > curdate()


  -- Track My spending
  SELECT SUM(flight.price) as TotalSpending
    FROM purchases, ticket, flight
      WHERE purchases.customer_email = 'one@nyu.edu'
      AND purchases.ticket_id = ticket.ticket_id
      AND ticket.airline_name = flight.airline_name
      AND ticket.flight_num = flight.flight_num
      AND purchases.purchase_date BETWEEN date_sub('2020-01-01', INTERVAL 2 DAY) AND date_sub('2020-12-31', INTERVAL 2 DAY)
      GROUP BY purchases.customer_email


  -- Buy Ticket
  SELECT COUNT(*) AS count FROM ticket
    WHERE ticket.airline_name = 'Jet Blue' AND ticket.flight_num = '915'

  SELECT MAX(ticket_id) + 1 as nxt_ticket_id FROM ticket
    WHERE (SELECT COUNT(*) as count FROM ticket
            WHERE ticket.airline_name = 'Jet Blue' AND ticket.flight_num = '915'
          ) < (SELECT airplane.seats as seats FROM flight, airplane
                WHERE flight.airline_name = 'Jet Blue' AND flight.flight_num = '915'
                  AND flight.airplane_id = airplane.airplane_id)


  -- Spending Details
  SELECT SUM(flight.price) as spend, YEAR(purchases.purchase_date) as year, MONTH(purchases.purchase_date) as month
      FROM purchases, ticket, flight
        WHERE purchases.customer_email = 'one@nyu.edu'
        AND purchases.ticket_id = ticket.ticket_id
        AND ticket.airline_name = flight.airline_name
        AND ticket.flight_num = flight.flight_num
        AND purchases.purchase_date BETWEEN date_sub('2020-01-01', INTERVAL 2 DAY) AND date_sub('2020-12-31', INTERVAL 2 DAY)
      GROUP BY year, month
      ORDER BY purchases.purchase_date


  -- Search Ticket
  SELECT distinct f.airline_name,
                f.flight_num,
                departure_airport,
                departure_time,
                arrival_airport,
                arrival_time,
                price,
                airplane_id
            FROM flight as f, airport
            WHERE airport.airport_name=f.departure_airport
            AND airport.airport_city = 'San Francisco'
            AND airport.airport_name = 'SFO'
            AND f.departure_time BETWEEN DATE_SUB('2019-12-20', INTERVAL 2 DAY) AND DATE_ADD('2020-12-21', INTERVAL 2 DAY)
            AND (f.airline_name, f.flight_num) in
                (SELECT flight.airline_name, flight.flight_num FROM flight, airport
                    WHERE airport.airport_name=flight.arrival_airport
                      AND airport.airport_city = 'New York City'
                      AND airport.airport_name = 'JFK')
            AND (SELECT DISTINCT seats FROM flight, airplane
                    WHERE flight.airplane_id = airplane.airplane_id
                      AND flight.airline_name = airplane.airline_name
                      AND flight.airline_name = f.airline_name
                      AND flight.flight_num = f.flight_num) >=
                        (SELECT COUNT(*) FROM ticket
                            WHERE ticket.airline_name = f.airline_name
                              AND ticket.flight_num = f.flight_num)


------------------------------------------------------------------
-- Agent
  -- View Homepage
  SELECT ticket.ticket_id, ticket.airline_name, ticket.flight_num,
        departure_airport, departure_time, arrival_airport, arrival_time, airplane_id, status,
        price, customer_email, purchases.booking_agent_id, purchase_date
    FROM purchases, ticket, flight, booking_agent
      WHERE purchases.ticket_id = ticket.ticket_id
        AND ticket.airline_name = flight.airline_name
        AND ticket.flight_num   = flight.flight_num
        AND booking_agent.email = 'Booking@agent.com'
        AND booking_agent.booking_agent_id = purchases.booking_agent_id
        AND departure_time > curdate() ORDER BY customer_email

  SELECT SUM(price) as commission
    FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
    JOIN flight USING(airline_name, flight_num)
      WHERE purchase_date >= date_sub(curdate(), INTERVAL 1 MONTH)
        AND email='Booking@agent.com' GROUP by email

  SELECT COUNT(*) as sales
    FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
    JOIN flight USING(airline_name, flight_num)
      WHERE purchase_date >= date_sub(curdate(), INTERVAL 1 MONTH)
        AND email='Booking@agent.com' GROUP by email


  -- View commission
  SELECT SUM(price) as commission
  FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
  JOIN flight USING(airline_name, flight_num)
    WHERE purchase_date >= date_sub(curdate(), INTERVAL 1 MONTH)
      AND email='Booking@agent.com' GROUP by email

  SELECT COUNT(*) as sales
    FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
    JOIN flight USING(airline_name, flight_num)
      WHERE purchase_date >= date_sub(curdate(), INTERVAL 1 MONTH)
        AND email='Booking@agent.com' GROUP by email


  -- Rank Customer
  SELECT customer_email, COUNT(ticket_id) as sale
    FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
    JOIN flight USING(airline_name, flight_num)
      WHERE booking_agent.email = 'Booking@agent.com'
      AND purchase_date >= date_sub(curdate(), INTERVAL 1 YEAR)
      GROUP BY customer_email ORDER BY sale DESC LIMIT 5

  SELECT customer_email, SUM(price) as commission
    FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
    JOIN flight USING(airline_name, flight_num)
      WHERE booking_agent.email = 'Booking@agent.com'
      AND purchase_date >= date_sub(curdate(), INTERVAL 1 YEAR)
      GROUP by customer_email ORDER by commission DESC LIMIT 5


------------------------------------------------------------------
-- Staff
  -- View Homepage
  SELECT * FROM flight
    WHERE  airline_name = 'Jet Blue'
      AND (
            ( departure_time BETWEEN Curdate() AND Date_add(Curdate(), interval 30 day) )
            OR
            ( arrival_time BETWEEN Curdate() AND Date_add(Curdate(), interval 30 day) )
          )

  SELECT airport_city, COUNT(ticket_id) as count FROM airport, ticket JOIN flight USING(airline_name, flight_num)
      WHERE airport_name = arrival_airport
      AND airline_name='Jet Blue' GROUP by airport_city ORDER by count DESC

  UPDATE flight SET status='In-progress' where flight_num=102 and airline_name = 'Jet Blue'


  -- View Report
  SELECT YEAR(purchase_date) as year, MONTH(purchase_date) as month, COUNT(ticket_id) as sales
    FROM purchases NATURAL JOIN ticket JOIN flight USING(airline_name, flight_num)
      WHERE  airline_name = 'Jet Blue'
      AND purchase_date BETWEEN date_sub('2020-01-01', INTERVAL 2 DAY) AND date_sub('2020-12-31', INTERVAL 2 DAY)
    GROUP BY year, month

  SELECT *  FROM
  (SELECT SUM(price) as unagented FROM purchases NATURAL JOIN ticket JOIN flight USING(airline_name, flight_num)
      WHERE  airline_name = 'Jet Blue'
      AND purchase_date BETWEEN date_sub('2020-01-01', INTERVAL 2 DAY) AND date_sub('2020-12-31', INTERVAL 2 DAY)
      AND booking_agent_id IS NULL) as a,

    (SELECT SUM(price) as agented FROM purchases NATURAL JOIN ticket JOIN flight USING(airline_name, flight_num)
        WHERE  airline_name = 'Jet Blue'
        AND purchase_date BETWEEN date_sub('2020-01-01', INTERVAL 2 DAY) AND date_sub('2020-12-31', INTERVAL 2 DAY)
        AND booking_agent_id IS NOT NULL) as b


  -- View customer's flights
  SELECT ticket.flight_num FROM purchases, ticket, flight
    WHERE purchases.customer_email = 'one@nyu.edu'
      AND purchases.ticket_id = ticket.ticket_id
      AND ticket.airline_name = flight.airline_name
      AND flight.airline_name = 'Jet Blue'
      AND ticket.flight_num = flight.flight_num
      AND departure_time < curdate()
      AND purchases.purchase_date BETWEEN date_sub('2020-01-01', INTERVAL 2 DAY) AND date_sub('2020-12-31', INTERVAL 2 DAY)


  -- View most frequent customer_email
  SELECT customer_email, COUNT(ticket_id) as sale
    FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
    JOIN flight USING(airline_name, flight_num)
      WHERE flight.airline_name = 'Jet Blue'
      AND purchase_date >= date_sub(curdate(), INTERVAL 1 YEAR)
      GROUP BY customer_email ORDER BY sale


  -- Rank Agent
  SELECT email, COUNT(ticket_id) as sale
  FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
  JOIN flight USING(airline_name, flight_num)
    WHERE purchase_date >= date_sub(curdate(), INTERVAL 1 YEAR)
      AND airline_name='Jet Blue' GROUP BY email ORDER BY sale DESC

  SELECT email, SUM(price) as commission
    FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
    JOIN flight USING(airline_name, flight_num)
      WHERE purchase_date >= date_sub(curdate(), INTERVAL 1 YEAR)
        AND airline_name='Jet Blue' GROUP by email ORDER by commission DESC