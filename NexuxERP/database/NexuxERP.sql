DROP DATABASE IF EXISTS NexusERP
GO


CREATE DATABASE NexusERP
ON
(
	NAME = NexusERP_dat,
	FILENAME = 'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\NexusERP_dat.mdf',
	SIZE = 10MB,
	MAXSIZE = 50MB,
	FILEGROWTH = 5MB
)
LOG ON
(
	NAME = NexusERP_log,
	FILENAME = 'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\NexusERP_log.ldf',
	SIZE = 10MB,
	MAXSIZE = 50MB,
	FILEGROWTH = 5MB
)
GO

USE NexusERP
GO

CREATE TABLE ALMACENES(
	id_almacen INT PRIMARY KEY IDENTITY,
	nombre VARCHAR(100),
	ubicacion VARCHAR(100),
	archivo BIT
);

CREATE TABLE PRODUCTOS(
	id_producto INT PRIMARY KEY IDENTITY,
	sku VARCHAR(60) UNIQUE,
	nombre VARCHAR(150),
	tipo VARCHAR(20),
	unidad_medida VARCHAR(20),
	precio_compra DECIMAL(12,2),
	precio_venta DECIMAL(12,2),
	stock_minimo FLOAT,
	stock_maximo FLOAT
);

CREATE TABLE INVENTARIO_STOCK(
	id_stock INT PRIMARY KEY IDENTITY,
	id_almacen INT,
	id_producto INT,
	cantidad_actual FLOAT,
	FOREIGN KEY (id_almacen) REFERENCES ALMACENES(id_almacen),
	FOREIGN KEY (id_producto) REFERENCES PRODUCTOS(id_producto)
);

--PARTE 2--
CREATE TABLE PROVEEDORES(
	id_proveedor INT PRIMARY KEY IDENTITY,
	rfc_tax_id VARCHAR(20) UNIQUE,
	razon_social VARCHAR(150),
	telefono VARCHAR(15),
	email VARCHAR(30),
);

CREATE TABLE ORDENES_COMPRA(
	id_orden_compra INT PRIMARY KEY IDENTITY,
	id_proveedor INT,
	id_almacen_destino INT,
	fecha_emision DATE,
	status VARCHAR(20),
	total DECIMAL(12,2),
	FOREIGN KEY (id_proveedor) REFERENCES PROVEEDORES(id_proveedor),
	FOREIGN KEY (id_almacen_destino) REFERENCES ALMACENES(id_almacen)
);

CREATE TABLE DETALLE_COMPRA(
	id_detalle_compra INT PRIMARY KEY IDENTITY,
	id_orden_compra INT,
	id_producto INT,
	cantidad_pedida FLOAT,
	precio_unitario DECIMAL(12,2),
	FOREIGN KEY (id_orden_compra) REFERENCES ORDENES_COMPRA(id_orden_compra),
	FOREIGN KEY (id_producto) REFERENCES PRODUCTOS(id_producto)
);

--PARTE 3--
CREATE TABLE BOM_CABECERA(
	id_bom INT PRIMARY KEY IDENTITY,
	id_producto_terminado INT,
	version VARCHAR(10),
	descripcion VARCHAR(255)
);

CREATE TABLE BOM_DETALLES(
	id_bom_detalle INT PRIMARY KEY IDENTITY,
	id_bom INT,
	id_insumo INT,
	cantidad_requerida FLOAT,
	FOREIGN KEY (id_bom) REFERENCES BOM_CABECERA(id_bom),
	FOREIGN KEY (id_insumo) REFERENCES PRODUCTOS(id_producto)
);

CREATE TABLE ORDENES_PRODUCCION(
	id_orden_prod INT PRIMARY KEY IDENTITY,
	id_bom INT,
	id_almacen INT,
	cantidad_a_fabricar FLOAT,
	fecha_inicio DATETIME,
	fecha_fin DATETIME,
	status VARCHAR(30),
	FOREIGN KEY (id_bom) REFERENCES BOM_CABECERA(id_bom),
	FOREIGN KEY (id_almacen) REFERENCES ALMACENES(id_almacen)
);

--PARTE 4--
CREATE TABLE CLIENTES(
	id_cliente INT PRIMARY KEY IDENTITY,
	tipo_cliente VARCHAR(50),
	nombre_o_razon_social VARCHAR(50),
	rfc_o_tax_id VARCHAR(20) UNIQUE,
	telefono VARCHAR(15),
	email VARCHAR(50),
	direccion VARCHAR(255)
);

CREATE TABLE PEDIDOS_VENTA(
	id_pedido INT PRIMARY KEY IDENTITY,
	id_cliente INT,
	id_almacen_origen INT,
	fecha_pedido DATETIME,
	status VARCHAR(20),
	total DECIMAL(12,2),
	FOREIGN KEY (id_cliente) REFERENCES CLIENTES(id_cliente),
	FOREIGN KEY (id_almacen_origen) REFERENCES ALMACENES(id_almacen)
);

CREATE TABLE DETALLE_VENTA(
	id_detalle_venta INT PRIMARY KEY IDENTITY,
	id_pedido INT,
	id_producto INT,
	cantidad FLOAT,
	precio_unitario DECIMAL(12,2)
	FOREIGN KEY (id_pedido) REFERENCES PEDIDOS_VENTA(id_pedido),
	FOREIGN KEY (id_producto) REFERENCES PRODUCTOS(id_producto)
);

CREATE TABLE MOVIMIENTOS_KARDEX(
	id_kardex INT PRIMARY KEY IDENTITY,
	id_almacen INT,
	id_producto INT,
	tipo_movimiento VARCHAR(30),
	cantidad FLOAT,
	stock_resultante FLOAT,
	fecha DATETIME,
	id_referencia INT
	FOREIGN KEY (id_almacen) REFERENCES ALMACENES(id_almacen),
	FOREIGN KEY (id_producto) REFERENCES PRODUCTOS(id_producto)
);