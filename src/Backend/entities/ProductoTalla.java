package com.inventario.sistema.entities;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;
import jakarta.validation.constraints.Min;
import lombok.*;

@Entity
@Table(name = "producto_talla", uniqueConstraints = {
    @UniqueConstraint(columnNames = {"producto_id", "talla_id"})
})
@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})  
public class ProductoTalla {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(optional = false, fetch = FetchType.EAGER)  
    @JoinColumn(name = "producto_id", nullable = false)
    @JsonIgnoreProperties({"hibernateLazyInitializer", "handler"}) 
    private Producto producto;

    @ManyToOne(optional = false, fetch = FetchType.EAGER)  
    @JoinColumn(name = "talla_id", nullable = false)
    @JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
    private Talla talla;

    @Min(0)
    @Column(nullable = false)
    private Integer stockActual = 0;

    @Min(0)
    @Column(nullable = false)
    private Integer stockMinimo = 0;
}
