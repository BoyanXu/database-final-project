-- @app.route("/customerHome")
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



-- @app.route("/customerSearch")
-- Query Format: fromCity,      fromAirport, fromDate,   toDate,     toCity,        toAirport
-- Query Input: San Francisco, SFO,         2020-12-20, 2020-12-21, New York City, JFK
-- Response Format: airline_name, flight_num, departure_airport, departure_time, arrival_airport, airplane_id, arrival_time, price
-- Response Data  : Jet Blue,     139,        SFO,               2020-12-20,     JFK,             2020-12-21
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
            AND '2020-12-20' BETWEEN DATE_SUB(f.departure_time, INTERVAL 2 DAY) AND DATE_ADD(f.departure_time, INTERVAL 2 DAY)
            AND '2020-12-21' BETWEEN DATE_SUB(f.arrival_time, INTERVAL 2 DAY) AND DATE_ADD(f.arrival_time, INTERVAL 2 DAY)
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


-- app.route("/staffHome")
-- Query Format: airline_name
-- Query Input: Jet Blue
-- Response Format: airline_name,  flight_num,  departure_airport,  departure_time,  arrival_airport,  arrival_time,  price,  status,  airplane_id
-- Response Data: ..
SELECT * FROM flight
  WHERE  airline_name = 'Jet Blue'
    AND (
          ( departure_time BETWEEN Curdate() AND Date_add(Curdate(), interval 30 day) )
          OR
          ( arrival_time BETWEEN Curdate() AND Date_add(Curdate(), interval 30 day) )
        )

-- app.route("/customerHome/purchase/status")
-- Query Format: airline_name, flight_num
-- Query Input: Jet Blue,
SELECT COUNT(*) AS count FROM ticket
  WHERE ticket.airline_name = 'Jet Blue' AND ticket.flight_num = '915'
-- Response Format: count
-- Response Data: 3


-- app.route("/customerHome/purchase/status")
-- Query Format: airline_name, flight_num
-- Query Input: Jet Blue, 915
SELECT MAX(ticket_id) + 1 as nxt_ticket_id FROM ticket
  WHERE (SELECT COUNT(*) as count FROM ticket
          WHERE ticket.airline_name = 'Jet Blue' AND ticket.flight_num = '915'
        ) < (SELECT airplane.seats as seats FROM flight, airplane
              WHERE flight.airline_name = 'Jet Blue' AND flight.flight_num = '915'
                AND flight.airplane_id = airplane.airplane_id)
-- Response Format: nxt_ticket_id
-- Response Data: 10  (NULL if unsatisfied)




-- app.route("/agentHome")
-- Query Format: agentID
-- Query Input: Booking@agent.com,
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
-- Response Format: ticket_id, airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, airplane_id, status, price, customer_email, booking_agent_id, purchase_date
-- Response Data: ...


-- app.route("/staffHome/viewStaff/status")
-- Query Format: airlineName, range
-- Query Input: Jet Blue, MONTH
SELECT email, COUNT(ticket_id) as sale
  FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
  JOIN flight USING(airline_name, flight_num)
    WHERE purchase_date >= date_sub(curdate(), INTERVAL 1 YEAR)
      AND airline_name='Jet Blue' GROUP BY email ORDER BY sale DESC
-- Response Format: email, sale


-- app.route("/staffHome/viewStaff/status")
-- Query Format: range, airlineName
-- Query Input : YEAR,  Jet Blue
SELECT email, SUM(price) as commission
  FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
  JOIN flight USING(airline_name, flight_num)
    WHERE purchase_date >= date_sub(curdate(), INTERVAL 1 YEAR)
      AND airline_name='Jet Blue' GROUP by email ORDER by commission DESC
-- Response Format: email, commission

-- Query Format: Status, flight_num
-- Query Input: "In progress", 102
-- app.route("/staffHome")
UPDATE flight SET status='In-progress' where flight_num=102 and airline_name = 'Jet Blue'