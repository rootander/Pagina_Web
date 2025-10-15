package com.inventario.sistema.launcher;

import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Component;

import java.io.*;

@Component
public class PythonLauncher {

    @PostConstruct
    public void launchPythonApp() {
        try {
            
            String batPath = "C:/Users/usuario/Pictures/Sistema_inventario_biometrico/sistema/python/run_facial_app.bat";

            File batFile = new File(batPath);

            if (!batFile.exists()) {
                System.err.println("❌ El archivo .bat no existe en: " + batFile.getAbsolutePath());
                return;
            }

            System.out.println("🚀 Ejecutando el archivo .bat: " + batFile.getAbsolutePath());

            
            ProcessBuilder pb = new ProcessBuilder("cmd", "/c", "start", "", batFile.getAbsolutePath());
            pb.directory(batFile.getParentFile()); 

            Process process = pb.start();

            System.out.println("✅ facial_app.py lanzado correctamente desde .bat");

        } catch (IOException e) {
            System.err.println("❌ Error al lanzar facial_app.py desde .bat:");
            e.printStackTrace();
        }
    }
}
