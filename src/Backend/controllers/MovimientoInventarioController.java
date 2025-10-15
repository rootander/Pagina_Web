package com.inventario.sistema.controllers;

import com.inventario.sistema.entities.MovimientoInventario;
import com.inventario.sistema.services.MovimientoInventarioService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/movimientos")
@RequiredArgsConstructor
public class MovimientoInventarioController {

    private final MovimientoInventarioService movimientoService;

    private String getCurrentUsername() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || !auth.isAuthenticated() || auth.getPrincipal().equals("anonymousUser")) {
            return null;
        }
        return auth.getName();
    }

    @GetMapping
    public ResponseEntity<List<MovimientoInventario>> listar() {
        return ResponseEntity.ok(movimientoService.listarTodos());
    }

    @GetMapping("/{id}")
    public ResponseEntity<MovimientoInventario> obtener(@PathVariable Long id) {
        return movimientoService.obtenerPorId(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Map<String, Object>> crear(@RequestBody MovimientoInventario movimiento) {
        String username = getCurrentUsername();
        Map<String, Object> resp = new HashMap<>();
        if (username == null) {
            resp.put("error", "Usuario no autenticado");
            return ResponseEntity.status(401).body(resp);
        }

        try {
            MovimientoInventario movGuardado = movimientoService.guardarConUsuario(movimiento, username);
            return ResponseEntity.status(201).body(Map.of("movimiento", movGuardado));
        } catch (RuntimeException e) {
            resp.put("error", e.getMessage());
            return ResponseEntity.badRequest().body(resp);
        }
    }

    @PutMapping("/{id}")
    public ResponseEntity<Map<String, Object>> actualizar(@PathVariable Long id, @RequestBody MovimientoInventario movimiento) {
        String username = getCurrentUsername();
        Map<String, Object> resp = new HashMap<>();
        if (username == null) {
            resp.put("error", "Usuario no autenticado");
            return ResponseEntity.status(401).body(resp);
        }

        try {
            MovimientoInventario movActualizado = movimientoService.actualizarConUsuario(id, movimiento, username);
            return ResponseEntity.ok(Map.of("movimiento", movActualizado));
        } catch (RuntimeException e) {
            resp.put("error", e.getMessage());
            return ResponseEntity.badRequest().body(resp);
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Map<String, Object>> eliminar(@PathVariable Long id) {
        Map<String, Object> resp = new HashMap<>();
        return movimientoService.obtenerPorId(id)
                .map(m -> {
                    movimientoService.eliminar(id);
                    resp.put("mensaje", "Movimiento eliminado");
                    return ResponseEntity.ok(resp);
                })
                .orElseGet(() -> {
                    resp.put("error", "Movimiento no encontrado");
                    return ResponseEntity.status(404).body(resp);
                });
    }

    @GetMapping("/producto/{productoId}")
    public ResponseEntity<List<MovimientoInventario>> movimientosPorProducto(@PathVariable Long productoId) {
        return ResponseEntity.ok(movimientoService.obtenerPorProducto(productoId));
    }

    @GetMapping("/producto-talla/{productoTallaId}")
    public ResponseEntity<List<MovimientoInventario>> movimientosPorProductoTalla(@PathVariable Long productoTallaId) {
        return ResponseEntity.ok(movimientoService.obtenerPorProductoTalla(productoTallaId));
    }
}
