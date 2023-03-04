-- Keep a log of any SQL queries you execute as you solve the mystery.

-- to see what tables we have access to
.tables

-- Query for the crime scene reports from the given date and street
SELECT * FROM crime_scene_reports
WHERE day=28 AND month=7
AND street="Humphrey Street";

-- Query for the interviews the day of the theft and that mentions "bakery"
SELECT name, transcript FROM interviews
WHERE year="2021" AND month="7" AND day="28"
AND transcript LIKE '%bakery%';

-- Check who left the parking around 10 min after the time of the theft 10:15am
SELECT bakery_security_logs.minute, people.name
FROM bakery_security_logs
JOIN people ON bakery_security_logs.license_plate = people.license_plate
WHERE year = "2021" AND month = "7" AND day = "28" AND hour = "10"
AND activity = "exit";

-- Check who withdrew money from the atm at Leggett Street earlier that day
SELECT name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE year="2021" AND month="7" AND day="28"
AND atm_location = "Leggett Street" AND transaction_type = "withdraw";

-- Check who called for less then one minute the day of the theft
SELECT phone_calls.id, name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE year="2021" AND month="7" AND day="28"
AND duration<60;

-- Check who received a call for less then one minute the day of the theft
SELECT phone_calls.id, name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE year="2021" AND month="7" AND day="28"
AND duration<60;

-- Check where the first flight from fiftyville goes to
SELECT hour, minute, airports.city FROM flights
JOIN airports ON flights.destination_airport_id = airports.id
WHERE origin_airport_id IN (
SELECT id FROM airports
WHERE full_name = "Fiftyville Regional Airport")
AND year = "2021" AND month = "7" AND day = "29"
ORDER BY hour, minute LIMIT 1;

-- Find out who was on the plane
SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
WHERE year = "2021" AND month = "7" AND day = "29"
AND hour = "8" AND minute = "20";