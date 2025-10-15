package com.inventario.sistema.controllers;

import com.inventario.sistema.entities.Talla;
import com.inventario.sistema.services.TallaService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/tallas")
@RequiredArgsConstructor
public class TallaController {

    private final TallaService tallaService;

    @GetMapping
    public ResponseEntity<List<Talla>> listar() {
        return ResponseEntity.ok(tallaService.listarTodas());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Talla> obtener(@PathVariable Long id) {
        return tallaService.obtenerPorId(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Talla> crear(@RequestBody Talla talla) {
        if (tallaService.existePorNombre(talla.getNombre())) {
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity.ok(tallaService.guardar(talla));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Talla> actualizar(@PathVariable Long id, @RequestBody Talla talla) {
        return tallaService.obtenerPorId(id)
                .map(t -> {
                    t.setNombre(talla.getNombre());
                    return ResponseEntity.ok(tallaService.guardar(t));
                }).orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminar(@PathVariable Long id) {
        if (!tallaService.obtenerPorId(id).isPresent()) {
            return ResponseEntity.notFound().build();
        }
        tallaService.eliminar(id);
        return ResponseEntity.noContent().build();
    }
}
