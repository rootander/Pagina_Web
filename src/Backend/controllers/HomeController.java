package com.inventario.sistema.controllers;

import com.inventario.sistema.entities.Producto;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
@RequiredArgsConstructor
@RequestMapping("/")
public class HomeController {

    @GetMapping
    public String redirigirALogin() {
        
        return "redirect:/esperando-login";
    }

    
    @GetMapping("/index")
    public String index() {
        return "pages/index"; 
    }

    @GetMapping("/esperando-login")
    @ResponseBody
    public String esperandoLogin() {
        return "Inicie sesión en la aplicación de Python para acceder al inventario...";
    }



}
