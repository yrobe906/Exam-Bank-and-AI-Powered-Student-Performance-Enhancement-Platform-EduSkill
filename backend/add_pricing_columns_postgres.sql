-- Add pricing columns to exams table for PostgreSQL
-- Run this SQL script on your PostgreSQL database

ALTER TABLE exams ADD COLUMN IF NOT EXISTS pricing_type VARCHAR(20) DEFAULT 'Free';
ALTER TABLE exams ADD COLUMN IF NOT EXISTS amount FLOAT DEFAULT 0;

-- Verify the columns were added
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'exams' 
AND column_name IN ('pricing_type', 'amount');
