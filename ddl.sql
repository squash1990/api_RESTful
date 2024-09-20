DROP DATABASE if exists db;
CREATE DATABASE db;
\connect db;

CREATE EXTENSION "uuid-ossp";
CREATE TABLE productos (
   sku uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
   price money,
   title varchar(80),
   long_description text
);

INSERT INTO productos (price, title, long_description) VALUES
    (12.4, 'Ejemplo 1', 'Producto ejemplar 1'),
    (34.43, 'Ejemplo 2', 'Producto ejemplar 2'),
    (12.4, 'Ejemplo 3', 'Producto ejemplar 3'),
    (34.43, 'Ejemplo 4', 'Producto ejemplar 4'),
    (12.4, 'Ejemplo 5', 'Producto ejemplar 5'),
    (34.43, 'Ejemplo 6', 'Producto ejemplar 6');
