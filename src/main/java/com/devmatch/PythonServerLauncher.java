package com.devmatch;

/**
 * DevMatch AI - Java Server Launcher
 * Este programa Java lanza y gestiona el servidor Flask de Python
 * Actualizado para Java 21 con características modernas
 * 
 * Autor: Caleb Nehemias
 * Fecha: Octubre 2025
 */

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.util.Scanner;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class PythonServerLauncher {
    
    private static final Logger logger = LoggerFactory.getLogger(PythonServerLauncher.class);
    
    private static final String PYTHON_SCRIPT = "app.py";
    private static final String SERVER_URL = "http://localhost:3000";
    private static final int MAX_STARTUP_WAIT = 30; // segundos
    private static final String VENV_PYTHON = ".venv/bin/python";
    
    private static Process pythonProcess;
    private static boolean serverRunning = false;
    private static final HttpClient httpClient = HttpClient.newBuilder()
        .connectTimeout(Duration.ofSeconds(2))
        .build();
    
    public static void main(String[] args) {
        var launcher = new PythonServerLauncher();
        launcher.run();
    }
    
    public void run() {
        System.out.println("===========================================");
        System.out.println("   DevMatch AI - Java Server Launcher");
        System.out.println("   Running on Java " + System.getProperty("java.version"));
        System.out.println("===========================================");
        System.out.println();
        
        // Configurar hook para shutdown limpio usando try-with-resources pattern
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            logger.info("Cerrando servidor...");
            System.out.println("\n🛑 Cerrando servidor...");
            stopPythonServer();
        }));
        
        try {
            // Verificar que existe el archivo Python usando Path API moderna
            Path pythonFile = Path.of(PYTHON_SCRIPT);
            if (!Files.exists(pythonFile)) {
                System.err.println("❌ Error: No se encuentra el archivo " + PYTHON_SCRIPT);
                System.exit(1);
            }
            
            // Lanzar servidor Python
            System.out.println("🚀 Iniciando servidor Flask de Python...");
            startPythonServer();
            
            // Esperar a que el servidor esté listo
            System.out.println("⏳ Esperando que el servidor esté listo...");
            waitForServerReady();
            
            if (serverRunning) {
                System.out.println("✅ ¡Servidor Flask iniciado correctamente!");
                System.out.println("🌐 Accede a: " + SERVER_URL);
                System.out.println();
                showMainMenu();
            } else {
                System.err.println("❌ Error: No se pudo iniciar el servidor Flask");
                System.exit(1);
            }
            
        } catch (Exception e) {
            logger.error("Error inesperado", e);
            System.err.println("❌ Error inesperado: " + e.getMessage());
            e.printStackTrace();
            stopPythonServer();
            System.exit(1);
        }
    }
    
    /**
     * Inicia el proceso del servidor Python Flask usando el entorno virtual
     */
    private void startPythonServer() throws IOException {
        // Verificar si existe el entorno virtual
        Path venvPython = Path.of(VENV_PYTHON);
        String pythonCommand;
        
        if (Files.exists(venvPython)) {
            pythonCommand = VENV_PYTHON;
            System.out.println("📦 Usando entorno virtual: " + VENV_PYTHON);
        } else {
            pythonCommand = "python3";
            System.out.println("⚠️  Entorno virtual no encontrado, usando Python del sistema");
        }
        
        var pb = new ProcessBuilder(pythonCommand, PYTHON_SCRIPT);
        pb.directory(Path.of(".").toFile()); // Directorio actual
        pb.redirectErrorStream(true); // Combinar stdout y stderr
        
        pythonProcess = pb.start();
        logger.info("Proceso Python iniciado con PID: {}", pythonProcess.pid());
        
        // Crear thread para leer la salida del proceso Python usando CompletableFuture
        CompletableFuture.runAsync(() -> {
            try (var reader = new BufferedReader(
                    new InputStreamReader(pythonProcess.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    // Mostrar salida del servidor Python con prefijo
                    System.out.println("🐍 Flask: " + line);
                    logger.debug("Flask output: {}", line);
                }
            } catch (IOException e) {
                logger.error("Error leyendo salida del servidor", e);
                System.err.println("Error leyendo salida del servidor: " + e.getMessage());
            }
        });
    }
    
    /**
     * Espera hasta que el servidor Flask esté respondiendo
     */
    private void waitForServerReady() {
        for (int i = 0; i < MAX_STARTUP_WAIT; i++) {
            try {
                if (isServerResponding()) {
                    serverRunning = true;
                    logger.info("Servidor Flask respondiendo correctamente");
                    return;
                }
                TimeUnit.SECONDS.sleep(1);
                System.out.print(".");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                logger.warn("Interrupción durante la espera del servidor");
                return;
            }
        }
        System.out.println();
        logger.warn("Timeout esperando respuesta del servidor");
    }
    
    /**
     * Verifica si el servidor Flask está respondiendo usando el nuevo HttpClient de Java 21
     */
    private boolean isServerResponding() {
        try {
            var request = HttpRequest.newBuilder()
                .uri(URI.create(SERVER_URL))
                .timeout(Duration.ofSeconds(2))
                .GET()
                .build();
            
            var response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            return response.statusCode() == 200;
        } catch (Exception e) {
            logger.debug("Servidor no responde aún: {}", e.getMessage());
            return false;
        }
    }
    
    /**
     * Muestra el menú principal con opciones usando pattern matching mejorado
     */
    private void showMainMenu() {
        try (var scanner = new Scanner(System.in)) {
            while (serverRunning) {
                System.out.println("""
                
                ===========================================
                           MENÚ DE CONTROL
                ===========================================
                1. 🌐 Abrir en navegador
                2. 📊 Ver estado del servidor
                3. 🔄 Reiniciar servidor
                4. 🛑 Detener servidor y salir
                ===========================================""");
                System.out.print("Selecciona una opción (1-4): ");
                
                try {
                    var input = scanner.nextLine().trim();
                    
                    switch (input) {
                        case "1" -> openInBrowser();
                        case "2" -> showServerStatus();
                        case "3" -> restartServer();
                        case "4" -> {
                            System.out.println("👋 ¡Hasta luego!");
                            serverRunning = false;
                        }
                        default -> System.out.println("⚠️  Opción no válida. Por favor selecciona 1-4.");
                    }
                } catch (Exception e) {
                    logger.error("Error procesando entrada", e);
                    System.err.println("❌ Error procesando entrada: " + e.getMessage());
                }
            }
        }
        
        stopPythonServer();
    }
    
    /**
     * Intenta abrir el servidor en el navegador predeterminado
     */
    private void openInBrowser() {
        try {
            var os = System.getProperty("os.name").toLowerCase();
            
            String command;
            if (os.contains("mac")) {
                command = "open " + SERVER_URL;
            } else if (os.contains("win")) {
                command = "rundll32 url.dll,FileProtocolHandler " + SERVER_URL;
            } else if (os.contains("nix") || os.contains("nux")) {
                command = "xdg-open " + SERVER_URL;
            } else {
                throw new UnsupportedOperationException("Sistema operativo no soportado: " + os);
            }
            
            Runtime.getRuntime().exec(command);
            System.out.println("🌐 Abriendo " + SERVER_URL + " en el navegador...");
            logger.info("Abriendo navegador para {}", SERVER_URL);
            
        } catch (IOException e) {
            logger.error("Error abriendo navegador", e);
            System.err.println("❌ Error abriendo navegador: " + e.getMessage());
            System.out.println("💡 Abre manualmente: " + SERVER_URL);
        }
    }
    
    /**
     * Muestra información del estado actual del servidor
     */
    private void showServerStatus() {
        var isResponding = isServerResponding();
        var isProcessAlive = pythonProcess != null && pythonProcess.isAlive();
        
        System.out.println("""
        
        📊 ESTADO DEL SERVIDOR:
           URL: %s
           Estado: %s
           Proceso Python: %s%s""".formatted(
            SERVER_URL,
            isResponding ? "🟢 Activo" : "🔴 Inactivo",
            isProcessAlive ? "🟢 Ejecutándose" : "🔴 Detenido",
            isProcessAlive ? "\n   PID: " + pythonProcess.pid() : ""
        ));
        
        logger.info("Estado del servidor - Respondiendo: {}, Proceso vivo: {}", 
                   isResponding, isProcessAlive);
    }
    
    /**
     * Reinicia el servidor Flask
     */
    private void restartServer() {
        System.out.println("🔄 Reiniciando servidor...");
        logger.info("Iniciando reinicio del servidor");
        
        // Detener servidor actual
        stopPythonServer();
        
        try {
            // Esperar un momento
            TimeUnit.SECONDS.sleep(2);
            
            // Reiniciar servidor
            startPythonServer();
            waitForServerReady();
            
            if (serverRunning) {
                System.out.println("✅ Servidor reiniciado correctamente!");
                logger.info("Servidor reiniciado exitosamente");
            } else {
                System.err.println("❌ Error reiniciando el servidor");
                logger.error("Error reiniciando el servidor");
                serverRunning = false;
            }
        } catch (Exception e) {
            logger.error("Error durante el reinicio", e);
            System.err.println("❌ Error durante el reinicio: " + e.getMessage());
            serverRunning = false;
        }
    }
    
    /**
     * Detiene el proceso del servidor Python
     */
    private void stopPythonServer() {
        if (pythonProcess != null && pythonProcess.isAlive()) {
            System.out.println("🛑 Deteniendo servidor Flask...");
            logger.info("Deteniendo proceso Python PID: {}", pythonProcess.pid());
            
            try {
                // Intentar terminar gracefully
                pythonProcess.destroy();
                
                // Esperar hasta 5 segundos para que termine
                if (!pythonProcess.waitFor(5, TimeUnit.SECONDS)) {
                    System.out.println("⚠️  Forzando cierre del servidor...");
                    logger.warn("Forzando cierre del proceso Python");
                    pythonProcess.destroyForcibly();
                }
                
                System.out.println("✅ Servidor Flask detenido");
                logger.info("Proceso Python detenido correctamente");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                logger.warn("Interrupción durante el cierre del proceso");
                pythonProcess.destroyForcibly();
            }
        }
        
        serverRunning = false;
    }
}