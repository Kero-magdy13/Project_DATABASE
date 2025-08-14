-- Create the database
CREATE DATABASE MedicineInventory;
USE MedicineInventory;

-- =========================
-- 1. Create Tables
-- =========================

-- Doctor Table
CREATE TABLE Doctor (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    doctor_name VARCHAR(100) NOT NULL,
    qualification VARCHAR(100),
    specialization VARCHAR(100) NOT NULL
);

-- Disease Table
CREATE TABLE Disease (
    disease_id INT PRIMARY KEY AUTO_INCREMENT,
    disease_name VARCHAR(100) NOT NULL,
    disease_type ENUM('infectious', 'deficiency', 'genetic hereditary', 'non-genetic hereditary') NOT NULL
);

-- Medicine Table
CREATE TABLE Medicine (
    medicine_id INT PRIMARY KEY AUTO_INCREMENT,
    medicine_name VARCHAR(100) NOT NULL,
    manufacture_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    dosage VARCHAR(50),
    disease_id INT,
    FOREIGN KEY (disease_id) REFERENCES Disease(disease_id)
);

-- Prescription Table
CREATE TABLE Prescription (
    prescription_id INT PRIMARY KEY AUTO_INCREMENT,
    doctor_id INT NOT NULL,
    patient_name VARCHAR(100) NOT NULL,
    issuing_date DATE NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id)
);

-- Prescription Details Table (many-to-many between Prescription & Medicine)
CREATE TABLE PrescriptionDetails (
    prescription_id INT,
    medicine_id INT,
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (prescription_id, medicine_id),
    FOREIGN KEY (prescription_id) REFERENCES Prescription(prescription_id) ON DELETE CASCADE,
    FOREIGN KEY (medicine_id) REFERENCES Medicine(medicine_id)
);

-- Bill Table
CREATE TABLE Bill (
    bill_id INT PRIMARY KEY AUTO_INCREMENT,
    prescription_id INT UNIQUE,
    tax DECIMAL(5,2) DEFAULT 0,
    discount DECIMAL(5,2) DEFAULT 0,
    total DECIMAL(10,2) DEFAULT 0,
    FOREIGN KEY (prescription_id) REFERENCES Prescription(prescription_id)
);

-- =========================
-- 2. Trigger to auto-update Bill
-- =========================

DELIMITER //
CREATE TRIGGER after_prescription_insert
AFTER INSERT ON PrescriptionDetails
FOR EACH ROW
BEGIN
    DECLARE subtotal DECIMAL(10,2);

    -- Calculate subtotal
    SELECT SUM(m.price * pd.quantity)
    INTO subtotal
    FROM PrescriptionDetails pd
    JOIN Medicine m ON pd.medicine_id = m.medicine_id
    WHERE pd.prescription_id = NEW.prescription_id;

    -- If bill exists, update it; else create it
    IF EXISTS (SELECT 1 FROM Bill WHERE prescription_id = NEW.prescription_id) THEN
        UPDATE Bill
        SET total = subtotal + (subtotal * tax / 100) - (subtotal * discount / 100)
        WHERE prescription_id = NEW.prescription_id;
    ELSE
        INSERT INTO Bill (prescription_id, tax, discount, total)
        VALUES (NEW.prescription_id, 5, 0, subtotal + (subtotal * 0.05));
    END IF;
END//
DELIMITER ;

-- =========================
-- 3. Insert Sample Data
-- =========================

-- Doctors
INSERT INTO Doctor (doctor_name, qualification, specialization) VALUES
('Dr. Ahmed Hassan', 'MBBS', 'Heart Disease'),
('Dr. Sara Ali', 'MD', 'Diabetes'),
('Dr. Omar Khaled', 'MBBS', 'Pediatrics'),
('Dr. Mona Youssef', 'MD', 'Heart Disease');

-- Diseases
INSERT INTO Disease (disease_name, disease_type) VALUES
('Heart Disease', 'non-genetic hereditary'),
('Diabetes', 'deficiency'),
('Flu', 'infectious'),
('Cystic Fibrosis', 'genetic hereditary');

-- Medicines
INSERT INTO Medicine (medicine_name, manufacture_date, expiry_date, price, dosage, disease_id) VALUES
('CardioPlus', '2023-01-01', '2025-01-01', 150.00, '1 tablet daily', 1),
('InsuMed', '2023-02-01', '2024-02-01', 100.00, 'Twice daily', 2),
('FluAway', '2023-03-01', '2024-03-01', 50.00, '3 times daily', 3),
('CystiCare', '2023-04-01', '2025-04-01', 200.00, '1 tablet daily', 4),
('HeartStrong', '2023-01-15', '2025-01-15', 180.00, '1 tablet daily', 1);

-- Prescriptions
INSERT INTO Prescription (doctor_id, patient_name, issuing_date) VALUES
(1, 'Mohamed Ali', '2023-05-01'),
(2, 'Fatma Hassan', '2023-05-02'),
(1, 'Ali Hassan', '2023-06-10');

-- Prescription Details
INSERT INTO PrescriptionDetails (prescription_id, medicine_id, quantity) VALUES
(1, 1, 2),
(1, 5, 1),
(2, 2, 1),
(3, 1, 3),
(3, 5, 2);

-- Manually insert bills (trigger will also update when new medicines added)
INSERT INTO Bill (prescription_id, tax, discount, total) VALUES
(1, 5, 0, 0),
(2, 5, 0, 0),
(3, 5, 0, 0);

-- =========================
-- 4. Example Queries
-- =========================

-- 1. List the name of doctors whose specialty is heart disease
SELECT doctor_name
FROM Doctor
WHERE specialization = 'Heart Disease';

-- 2. List the deficiency diseases
SELECT disease_name
FROM Disease
WHERE disease_type = 'deficiency';

-- 3. List the most sold medicine in 2023
SELECT m.medicine_name, SUM(pd.quantity) AS total_sold
FROM PrescriptionDetails pd
JOIN Medicine m ON pd.medicine_id = m.medicine_id
JOIN Prescription p ON pd.prescription_id = p.prescription_id
WHERE YEAR(p.issuing_date) = 2023
GROUP BY m.medicine_id
ORDER BY total_sold DESC
LIMIT 1;
