package com.inventario.sistema.controllers;

import com.inventario.sistema.entities.ProductoTalla;
import com.inventario.sistema.services.ProductoTallaService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/producto-talla")
@RequiredArgsConstructor
public class ProductoTallaController {

    private final ProductoTallaService productoTallaService;

    @GetMapping
    public ResponseEntity<List<ProductoTalla>> listar() {
        return ResponseEntity.ok(productoTallaService.listarTodos());
    }

    @GetMapping("/{id}")
    public ResponseEntity<ProductoTalla> obtener(@PathVariable Long id) {
        return productoTallaService.obtenerPorId(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/producto/{productoId}")
    public ResponseEntity<List<ProductoTalla>> porProducto(@PathVariable Long productoId) {
        return ResponseEntity.ok(productoTallaService.obtenerPorProducto(productoId));
    }

    @PostMapping
    public ResponseEntity<ProductoTalla> crear(@RequestBody ProductoTalla productoTalla) {
        if (productoTallaService.existePorProductoYPorTalla(
                productoTalla.getProducto().getId(), productoTalla.getTalla().getId())) {
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity.ok(productoTallaService.guardar(productoTalla));
    }

    @PutMapping("/{id}")
    public ResponseEntity<ProductoTalla> actualizar(@PathVariable Long id, @RequestBody ProductoTalla productoTalla) {
        return productoTallaService.obtenerPorId(id)
                .map(pt -> {
                    pt.setStockActual(productoTalla.getStockActual());
                    pt.setStockMinimo(productoTalla.getStockMinimo());
                    return ResponseEntity.ok(productoTallaService.guardar(pt));
                }).orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminar(@PathVariable Long id) {
        if (!productoTallaService.obtenerPorId(id).isPresent()) {
            return ResponseEntity.notFound().build();
        }
        productoTallaService.eliminar(id);
        return ResponseEntity.noContent().build();
    }
}
