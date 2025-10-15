package com.inventario.sistema.controllers;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import com.inventario.sistema.services.EmpleadoService;
import com.inventario.sistema.services.MovimientoInventarioService;
import com.inventario.sistema.services.ProductoService;
import com.inventario.sistema.services.ProductoTallaService;

import jakarta.servlet.http.HttpServletResponse;

@Controller
@RequiredArgsConstructor
public class PageController {

    private final ProductoTallaService productoTallaService;
    private final ProductoService productoService;
    private final MovimientoInventarioService movimientoService;
    private final EmpleadoService empleadoService;
@GetMapping("/dashboard")
public String dashboard(Model model, HttpServletResponse response) {
    response.setHeader("Cache-Control", "no-cache, no-store, must-revalidate");
    response.setHeader("Pragma", "no-cache");
    response.setDateHeader("Expires", 0);

    try {
        long totalInventario = productoTallaService.contarTotal();
        long totalProductos = productoService.contarActivos();
        long totalMovimientos = movimientoService.contarEsteMes();
        long totalEmpleados = empleadoService.contar();

        model.addAttribute("totalInventario", totalInventario);
        model.addAttribute("totalProductos", totalProductos);
        model.addAttribute("totalMovimientos", totalMovimientos);
        model.addAttribute("totalEmpleados", totalEmpleados);

    } catch (Exception e) {
        System.err.println("Error al obtener datos del dashboard: " + e.getMessage());
        model.addAttribute("error", "Hubo un error al cargar los datos del dashboard.");
    }

    return "pages/dashboard";
}


    @GetMapping("/productos")
    public String verProductos() {
        return "pages/productos";
    }

    @GetMapping("/inventario")
    public String verInventario() {
        return "pages/inventario";
    }

    @GetMapping("/movimientos")
    public String verMovimientos() {
        return "pages/movimientos";
    }
    @GetMapping("/empleados")
public String verEmpleados() {
    return "pages/empleados";
}
@GetMapping("/categorias")
public String verCategorias() {
    return "pages/categorias"; 
}
 @GetMapping("/proveedores")
    public String verProveedores() {
        return "pages/proveedores"; 
    }

}
