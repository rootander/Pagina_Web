# Tabla: producto_talla

```sql
CREATE TABLE producto_talla (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    producto_id BIGINT NOT NULL,
    talla_id BIGINT NOT NULL,
    stock_actual INT NOT NULL DEFAULT 0,
    stock_minimo INT NOT NULL DEFAULT 0,

    UNIQUE (producto_id, talla_id),

    CONSTRAINT fk_producto_talla_producto
        FOREIGN KEY (producto_id)
        REFERENCES productos(id),

    CONSTRAINT fk_producto_talla_talla
        FOREIGN KEY (talla_id)
        REFERENCES tallas(id)
);
```
