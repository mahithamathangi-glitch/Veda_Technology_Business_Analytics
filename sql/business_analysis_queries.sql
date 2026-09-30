-- ==========================================================
-- VEDA TECHNOLOGY BUSINESS & SERVICE ANALYTICS
-- SQL ANALYSIS QUERIES
-- ==========================================================


-- ==========================================================
-- 1. TOTAL WEBSITE VISITORS
-- ==========================================================

SELECT
    SUM(Website_Visit) AS Total_Website_Visitors
FROM business_data;


-- ==========================================================
-- 2. TOTAL SERVICE REQUESTS
-- ==========================================================

SELECT
    SUM(Service_Request) AS Total_Service_Requests
FROM business_data;


-- ==========================================================
-- 3. TOTAL REVENUE
-- ==========================================================

SELECT
    SUM(Revenue) AS Total_Revenue
FROM business_data;


-- ==========================================================
-- 4. MARKETING CHANNEL PERFORMANCE
-- ==========================================================

SELECT
    Marketing_Channel,
    SUM(Website_Visit) AS Visitors,
    SUM(Conversion) AS Conversions,
    SUM(Revenue) AS Revenue
FROM business_data
GROUP BY Marketing_Channel
ORDER BY Revenue DESC;


-- ==========================================================
-- 5. SERVICE DEMAND
-- ==========================================================

SELECT
    Service,
    SUM(Service_Request) AS Total_Requests
FROM business_data
GROUP BY Service
ORDER BY Total_Requests DESC;


-- ==========================================================
-- 6. CUSTOMER TYPE ANALYSIS
-- ==========================================================

SELECT
    Customer_Type,
    COUNT(*) AS Number_of_Customers,
    SUM(Revenue) AS Revenue,
    AVG(Satisfaction_Score) AS Average_Satisfaction
FROM business_data
GROUP BY Customer_Type
ORDER BY Revenue DESC;


-- ==========================================================
-- 7. SERVICE RESPONSE TIME
-- ==========================================================

SELECT
    Service,
    AVG(Response_Time_Hours) AS Average_Response_Time
FROM business_data
GROUP BY Service
ORDER BY Average_Response_Time DESC;


-- ==========================================================
-- 8. TRAINING PROGRAM PERFORMANCE
-- ==========================================================

SELECT
    Training_Program,
    SUM(Training_Enrollment) AS Enrollments,
    SUM(Training_Completion) AS Completions,
    AVG(Training_Score) AS Average_Score
FROM business_data
GROUP BY Training_Program
ORDER BY Average_Score DESC;


-- ==========================================================
-- 9. INTERNSHIP APPLICATION ANALYSIS
-- ==========================================================

SELECT
    Application_Status,
    COUNT(*) AS Number_of_Applications
FROM business_data
WHERE Inquiry_Type = 'Internship'
GROUP BY Application_Status
ORDER BY Number_of_Applications DESC;


-- ==========================================================
-- 10. CUSTOMER SATISFACTION
-- ==========================================================

SELECT
    AVG(Satisfaction_Score) AS Overall_Average_Satisfaction
FROM business_data;