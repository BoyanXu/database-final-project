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