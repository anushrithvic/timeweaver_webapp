CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'faculty', 'student')),
    full_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed initial admin user if not exists (password: 123)
-- Hash for '123' is likely '$2b$10$...' generated via bcrypt, but for raw SQL we'll handle this in the app logic or seed script.
-- For now, just the schema.
