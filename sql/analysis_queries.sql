-- name: top_10_strongest
SELECT place, mag
FROM earthquakes
ORDER BY mag DESC
LIMIT 10;

-- name: top_10_depth_earthquakes
SELECT place, depth_km
FROM earthquakes
ORDER BY depth_km DESC
LIMIT 10;

-- name: shallow_strong_earthquakes
SELECT *
FROM earthquakes
WHERE depth_km < 50 AND mag > 7.5;

-- name: avg_depth_country
SELECT 
    country,
    ROUND(AVG(depth_km),2) AS avg_depth_km
FROM earthquakes
GROUP BY country
ORDER BY avg_depth_km DESC;

-- name: avg_mag_country
SELECT country, AVG(mag) AS avg_mag
FROM earthquakes
GROUP BY country
ORDER BY avg_mag DESC;

-- name: year_with_most_earthquakes
SELECT year, COUNT(*) AS total
FROM earthquakes
GROUP BY year
ORDER BY total DESC;

-- name: month_highest_earthquakes
SELECT 
    CASE month
        WHEN 1 THEN 'January'
        WHEN 2 THEN 'February'
        WHEN 3 THEN 'March'
        WHEN 4 THEN 'April'
        WHEN 5 THEN 'May'
        WHEN 6 THEN 'June'
        WHEN 7 THEN 'July'
        WHEN 8 THEN 'August'
        WHEN 9 THEN 'September'
        WHEN 10 THEN 'October'
        WHEN 11 THEN 'November'
        WHEN 12 THEN 'December'
    END AS month_name,
    COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY month
ORDER BY total_earthquakes DESC;

-- name: day_of_week_most_earthquakes
SELECT 
    day_of_week,
    COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY day_of_week
ORDER BY total_earthquakes DESC;

-- name: count_earthquakes_per_hours_day
SELECT 
    EXTRACT(HOUR FROM time) AS hour_of_day,
    COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY hour_of_day;

-- name: most_active_net_work
SELECT 
    net,
    COUNT(*) AS total_reports
FROM earthquakes
GROUP BY net
ORDER BY total_reports DESC;

-- name: top_five_place
SELECT 
    place,
    MAX(mag) AS highest_magnitude
FROM earthquakes
GROUP BY place
ORDER BY highest_magnitude DESC
LIMIT 5;

-- name: total_estimated
SELECT 
    depth_category,
    COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY depth_category
ORDER BY total_earthquakes DESC;

-- name: avg_eco_loss
SELECT 
    country,
    AVG(mag) AS avg_magnitude
FROM earthquakes
GROUP BY country
ORDER BY avg_magnitude DESC;

-- name: count_review_earthquakes
SELECT 
    status,
    COUNT(*) AS total_events
FROM earthquakes
GROUP BY status;

-- name: count_earthquakes_type
SELECT 
    type,
    COUNT(*) AS total_events
FROM earthquakes
GROUP BY type
ORDER BY total_events DESC;

-- name: number_earthquakes
SELECT 
    types,
    COUNT(*) AS total_events
FROM earthquakes
GROUP BY types
ORDER BY total_events DESC;

-- name: avg_RMS_GAP
SELECT 
    country,
    AVG(rms) AS avg_rms,
    AVG(gap) AS avg_gap
FROM earthquakes
GROUP BY country
ORDER BY avg_rms DESC;

-- name: high_station_coverage
SELECT *
FROM earthquakes
WHERE nst > 100
ORDER BY nst DESC;

-- name: tsunami_count_per_year
SELECT year, COUNT(*) AS tsunami_events
FROM earthquakes
WHERE tsunami = 1
GROUP BY year;

-- name: alert_level
SELECT 
    CASE 
        WHEN mag >= 6 THEN 'Red'
        WHEN mag >= 4 AND mag < 6 THEN 'Orange'
        ELSE 'Yellow'
    END AS alert_color,
    COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY alert_color
ORDER BY total_earthquakes DESC;

-- name: highest_average_magnitude_10_years
SELECT 
    country,
    AVG(mag) AS avg_magnitude
FROM earthquakes
WHERE year >= EXTRACT(YEAR FROM CURRENT_DATE) - 10
GROUP BY country
ORDER BY avg_magnitude DESC
LIMIT 5;

-- name: shallow_and_deep
SELECT 
    country,
    year,
    month
FROM earthquakes
GROUP BY country, year, month
HAVING 
    SUM(CASE WHEN depth_category='Shallow' THEN 1 ELSE 0 END) > 0
AND 
    SUM(CASE WHEN depth_category='Deep' THEN 1 ELSE 0 END) > 0;

-- name: year_over_year_growth_rate
WITH yearly_counts AS (
SELECT year, COUNT(*) AS total
FROM earthquakes
GROUP BY year
)
SELECT 
    year, 
    total,
    LAG(total) OVER (ORDER BY year) as prev_year_total,
    ((total - LAG(total) OVER (ORDER BY year)) / LAG(total) OVER (ORDER BY year)) * 100 AS growth_rate
FROM yearly_counts;

-- name: most_3_seismically_active_regions
SELECT 
    country,
    COUNT(*) AS frequency,
    AVG(mag) AS avg_magnitude,
    (COUNT(*) * AVG(mag)) AS activity_score
FROM earthquakes
GROUP BY country
ORDER BY activity_score DESC
LIMIT 3;

-- name: avg_depth
SELECT 
    country,
    AVG(depth_km) AS avg_depth
FROM earthquakes
WHERE latitude BETWEEN -5 AND 5
GROUP BY country;


-- name: highest_ratio
SELECT 
    country,
    SUM(CASE WHEN depth_category='Shallow' THEN 1 ELSE 0 END) /
    SUM(CASE WHEN depth_category='Deep' THEN 1 ELSE 0 END) AS shallow_deep_ratio
FROM earthquakes
GROUP BY country
ORDER BY shallow_deep_ratio DESC;

-- name: average_magnitude
SELECT 
    tsunami,
    AVG(mag) AS avg_magnitude
FROM earthquakes
GROUP BY tsunami;

-- name: lowest_data_reliability
SELECT 
    id,
    place,
    gap,
    rms,
    (gap + rms) AS error_score
FROM earthquakes
ORDER BY error_score DESC
LIMIT 10;

-- name: one_hours_within_50km
SELECT 
    e1.id AS event1,
    e2.id AS event2,
    e1.place,
    e1.time AS time_1,
    e2.time AS time_2
FROM earthquakes e1
JOIN earthquakes e2
ON e1.id < e2.id
AND TIMESTAMPDIFF(MINUTE, e1.time, e2.time) <= 60
AND ABS(e1.latitude - e2.latitude) <= 0.3
AND ABS(e1.longitude - e2.longitude) <= 0.3
WHERE e1.mag >= 5
LIMIT 100;

-- name: determine_regions_with_the_highest_frequency
SELECT 
    country,
    COUNT(*) AS deep_earthquakes
FROM earthquakes
WHERE depth_km > 300
GROUP BY country
