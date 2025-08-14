-- Create the database
CREATE DATABASE IF NOT EXISTS ml_financial;
USE ml_financial;

-- Table: Company Analysis
CREATE TABLE IF NOT EXISTS analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id VARCHAR(20) NOT NULL UNIQUE,
    pros TEXT,
    cons TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
