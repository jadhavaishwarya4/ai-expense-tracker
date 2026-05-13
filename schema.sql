-- ============================================================
-- Personal Expense Tracker & Budget Management System
-- Database Schema (MySQL)
-- ============================================================

CREATE DATABASE IF NOT EXISTS expense_tracker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE expense_tracker;

-- ============================================================
-- USERS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    currency VARCHAR(10) DEFAULT 'INR',
    theme VARCHAR(10) DEFAULT 'dark',
    monthly_goal DECIMAL(12, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- ============================================================
-- CATEGORIES TABLE (static + user-defined)
-- ============================================================
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    icon VARCHAR(10) DEFAULT '💰',
    color VARCHAR(20) DEFAULT '#6366f1',
    user_id INT DEFAULT NULL,  -- NULL = system category
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert default categories
INSERT IGNORE INTO categories (id, name, icon, color) VALUES
(1, 'Food', '🍔', '#f59e0b'),
(2, 'Transport', '🚗', '#3b82f6'),
(3, 'Shopping', '🛍️', '#ec4899'),
(4, 'Bills', '📄', '#ef4444'),
(5, 'Entertainment', '🎬', '#8b5cf6'),
(6, 'Health', '💊', '#10b981'),
(7, 'Education', '📚', '#6366f1'),
(8, 'Others', '💡', '#64748b');

-- ============================================================
-- EXPENSES TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    date DATE NOT NULL,
    is_recurring BOOLEAN DEFAULT FALSE,
    receipt_path VARCHAR(500) DEFAULT NULL,
    tags VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, date),
    INDEX idx_user_category (user_id, category),
    INDEX idx_date (date)
);

-- ============================================================
-- INCOME TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS income (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    source VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    date DATE NOT NULL,
    is_recurring BOOLEAN DEFAULT FALSE,
    frequency VARCHAR(20) DEFAULT 'monthly', -- monthly, weekly, one-time
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, date)
);

-- ============================================================
-- BUDGETS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS budgets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    month INT NOT NULL,        -- 1-12
    year INT NOT NULL,
    alert_threshold DECIMAL(5, 2) DEFAULT 80.00,  -- alert at 80% usage
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_budget (user_id, category, month, year),
    INDEX idx_user_month_year (user_id, month, year)
);

-- ============================================================
-- SAVINGS GOALS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS savings_goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    goal_name VARCHAR(100) NOT NULL,
    target_amount DECIMAL(12, 2) NOT NULL,
    current_amount DECIMAL(12, 2) DEFAULT 0.00,
    deadline DATE,
    icon VARCHAR(10) DEFAULT '🎯',
    status VARCHAR(20) DEFAULT 'active',  -- active, completed, paused
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================
-- SAMPLE DATA (for demo)
-- ============================================================
-- This is handled in Python seed script
