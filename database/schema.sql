CREATE DATABASE IF NOT EXISTS insightflow_ai;

USE insightflow_ai;

DROP TABLE IF EXISTS customer_reviews;
DROP TABLE IF EXISTS crm_customers;
DROP TABLE IF EXISTS sales_transactions;
DROP TABLE IF EXISTS insight_feedback;

CREATE TABLE sales_transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    region VARCHAR(50) NOT NULL,
    product VARCHAR(100) NOT NULL,
    orders INT NOT NULL,
    revenue DECIMAL(12,2) NOT NULL,
    marketing_spend DECIMAL(12,2) NOT NULL
);

CREATE TABLE crm_customers (
    customer_id INT PRIMARY KEY,
    region VARCHAR(50) NOT NULL,
    churn BOOLEAN NOT NULL,
    signup_date DATE NOT NULL
);

CREATE TABLE customer_reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    review_date DATETIME NOT NULL,
    product VARCHAR(100) NOT NULL,
    rating INT NOT NULL,
    review_text TEXT NOT NULL
);

CREATE TABLE insight_feedback (
    feedback_id INT PRIMARY KEY AUTO_INCREMENT,
    insight_text TEXT,
    persona VARCHAR(50),
    rating VARCHAR(20),
    correction TEXT,
    confidence_score INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);