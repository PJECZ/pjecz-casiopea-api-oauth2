-- SQL de migración a la versión v1.4.0 para añadir el campo codigo_barras
-- a la tabla cit_citas.

-- Añadir la columna a la tabla existente
ALTER TABLE cit_citas 
ADD COLUMN codigo_barras VARCHAR(13);

-- Crear la restricción para asegurar que nunca se repitan
ALTER TABLE cit_citas 
ADD CONSTRAINT cit_citas_codigo_barras_unique UNIQUE (codigo_barras);

-- Añadir la columna a la tabla existente
ALTER TABLE cit_citas 
ADD COLUMN codigo_barras_url VARCHAR(512);