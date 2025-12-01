import java.io.IOException;
import java.nio.file.*;
import java.util.ArrayList;
import java.util.List;

public class RenombrarImagenes {

    public static void main(String[] args) {
        // 1. Definir la ruta de la carpeta
        
        String rutaCarpeta = "jetson_nano";
        Path directorio = Paths.get(rutaCarpeta);

        // Validar que la carpeta existe
        if (!Files.exists(directorio) || !Files.isDirectory(directorio)) {
            System.err.println("Error: La carpeta '" + rutaCarpeta + "' no existe o no es un directorio.");
            return;
        }

        System.out.println("Iniciando renombrado en: " + directorio.toAbsolutePath());

        try {
            // 2. Obtener todos los archivos .jpg
            // Usamos un DirectoryStream para filtrar eficientemente por extensión
            List<Path> archivosJpg = new ArrayList<>();
            try (DirectoryStream<Path> stream = Files.newDirectoryStream(directorio, "*.jpg")) {
                for (Path entry : stream) {
                    archivosJpg.add(entry);
                }
            }

            // 3. Recorrer y renombrar
            int contador = 1;
            for (Path archivoOriginal : archivosJpg) {
                // Crear el nuevo nombre: "1.jpg", "2.jpg", etc.
                String nuevoNombreArchivo = contador + ".jpg";
                Path rutaDestino = directorio.resolve(nuevoNombreArchivo);

                // Evitar sobreescribir si el archivo ya se llama "1.jpg" (por si corres el script 2 veces)
                if (archivoOriginal.getFileName().toString().equals(nuevoNombreArchivo)) {
                    System.out.println("El archivo " + nuevoNombreArchivo + " ya tiene el nombre correcto. Saltando...");
                    contador++;
                    continue;
                }

                // Ejecutar el cambio de nombre
                Files.move(archivoOriginal, rutaDestino, StandardCopyOption.REPLACE_EXISTING);
                
                System.out.println("Renombrado: " + archivoOriginal.getFileName() + " -> " + nuevoNombreArchivo);
                contador++;
            }

            System.out.println("--- Proceso finalizado exitosamente ---");

        } catch (IOException e) {
            System.err.println("Ocurrió un error al manipular los archivos: " + e.getMessage());
            e.printStackTrace();
        }
    }
}