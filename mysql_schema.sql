-- MySQL 마이그레이션 스키마
-- suntalk_backend 데이터베이스

CREATE DATABASE IF NOT EXISTS suntalk
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE suntalk;

-- 사용자 테이블
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    nickname VARCHAR(255),
    email VARCHAR(255),
    gender ENUM('male', 'female', 'other'),
    age INT,
    region_addr VARCHAR(500),
    kakao_id VARCHAR(255),
    naver_id VARCHAR(255),
    google_id VARCHAR(255),
    apple_id VARCHAR(255),
    thumbnail_url TEXT,
    background_image_url TEXT,
    points BIGINT DEFAULT 0,
    is_blocked BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_name (name),
    INDEX idx_users_email (email),
    INDEX idx_users_kakao_id (kakao_id),
    INDEX idx_users_naver_id (naver_id),
    INDEX idx_users_google_id (google_id),
    INDEX idx_users_apple_id (apple_id),
    INDEX idx_users_is_blocked (is_blocked)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 결제 정보 테이블
CREATE TABLE IF NOT EXISTS payments (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    amount INT NOT NULL,
    points_earned INT DEFAULT 0,
    payment_method ENUM('card', 'kakao_pay', 'naver_pay', 'apple_pay', 'google_pay', 'bank_transfer', 'other') NOT NULL,
    purpose ENUM('subscription', 'item_purchase', 'gift', 'donation', 'coin_purchase', 'other') NOT NULL,
    description TEXT,
    status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'completed',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_payments_user_id (user_id),
    INDEX idx_payments_created_at (created_at DESC),
    INDEX idx_payments_payment_method (payment_method),
    INDEX idx_payments_purpose (purpose)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;