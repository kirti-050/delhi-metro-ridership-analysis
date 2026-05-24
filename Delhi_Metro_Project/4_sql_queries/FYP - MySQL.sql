CREATE DATABASE Delhi_metro_project;
USE Delhi_metro_project;

UPDATE delhi_metro
SET Proper_date = STR_TO_DATE(DATE, '%Y-%m-%d');

SELECT DATE, Proper_date FROM delhi_metro LIMIT 5;

SELECT * FROM delhi_metro LIMIT 10;

SELECT
COUNT(*) AS Total_Trips,
SUM(Passengers) as Total_Passengers,
ROUND(SUM(Fare * Passengers), 2) AS Total_Revenue,
ROUND(AVG(Fare), 2) AS Average_Fare,
ROUND(AVG(Passengers), 2) AS Average_Passengers_Per_Trip,
ROUND(AVG(Distance_km), 2) AS Average_Distance_km,
MAX(Fare) AS Highest_Fare,
MIN(Fare) AS Lowest_Fare
FROM delhi_metro;

SELECT
Ticket_Type, 
COUNT(*) AS Total_Trips,
ROUND(AVG(Fare), 2) AS Average_Fare,
SUM(Passengers) AS Total_Passengers,
ROUND(SUM(Fare * Passengers), 2) AS Total_Revenue
FROM delhi_metro
GROUP BY Ticket_Type
ORDER BY Total_Revenue DESC;

SELECT 
From_Station,
COUNT(*) AS Total_Trips,
SUM(Passengers) AS Total_Passengers,
ROUND(AVG(Fare), 2) AS Average_Fare,
ROUND(SUM(Fare * Passengers), 2) AS Total_Revenue
FROM delhi_metro
GROUP BY From_Station
ORDER BY Total_Passengers DESC
LIMIT 10;

SELECT 
YEAR(Proper_Date) AS Year,
MONTH(Proper_Date) AS Month,
COUNT(*) AS Total_Trips,
SUM(Passengers) AS Total_Passengers,
ROUND(SUM(Fare * Passengers), 2) AS Total_Revenue
FROM delhi_metro
GROUP BY YEAR(Proper_Date), MONTH(Proper_Date)
ORDER BY Year, Month;

SELECT
Remarks,
COUNT(*) AS Total_Trips,
SUM(Passengers) AS Total_Passengers,
ROUND(AVG(Fare), 2) AS Average_Fare,
ROUND(SUM(Fare * Passengers), 2) AS Total_Revenue,
ROUND(AVG(Passengers), 2) AS Average_Passengers_Per_Trip
FROM delhi_metro
GROUP BY Remarks
ORDER BY Total_Passengers DESC;
