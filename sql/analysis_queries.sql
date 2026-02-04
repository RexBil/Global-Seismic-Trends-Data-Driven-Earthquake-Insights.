-- Top 10 strongest earthquakes
SELECT place, mag
FROM earthquakes
ORDER BY mag DESC
LIMIT 10;

-- Year with most earthquakes
SELECT year, COUNT(*) AS total
FROM earthquakes
GROUP BY year
ORDER BY total DESC;

-- Shallow & strong earthquakes
SELECT *
FROM earthquakes
WHERE depth_km < 50 AND mag > 7.5;

-- Tsunami count per year
SELECT year, COUNT(*) AS tsunami_events
FROM earthquakes
WHERE tsunami = 1
GROUP BY year;

-- Average magnitude per country
SELECT country, AVG(mag) AS avg_mag
FROM earthquakes
GROUP BY country
ORDER BY avg_mag DESC;
