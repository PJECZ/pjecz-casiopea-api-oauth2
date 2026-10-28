-- SQL de migración a la versión v1.5.0 para añadir el campo limite_personas
-- a la tabla cit_oficinas_servicios.

-- Añadir la columna con valor por omisión de 1
ALTER TABLE cit_oficinas_servicios
ADD COLUMN limite_personas INTEGER NOT NULL DEFAULT 1;
