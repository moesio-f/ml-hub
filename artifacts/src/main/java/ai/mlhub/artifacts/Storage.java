package ai.mlhub.artifacts;

import java.io.IOException;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.stream.Collectors;

import org.apache.commons.io.FileUtils;
import org.springframework.web.multipart.MultipartFile;

import com.fasterxml.jackson.core.PrettyPrinter;
import com.fasterxml.jackson.core.exc.StreamReadException;
import com.fasterxml.jackson.core.util.DefaultPrettyPrinter;
import com.fasterxml.jackson.databind.DatabindException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class Storage {
    private static Storage instance;
    private static ObjectMapper mapper = new ObjectMapper();
    private static PrettyPrinter printer = new DefaultPrettyPrinter().withoutSpacesInObjectEntries();
    private static Path modelDir = Path.of("models").toAbsolutePath();
    private static Path datasetDir = Path.of("datasets").toAbsolutePath();

    private final HashMap<String, Path> models;
    private final HashMap<String, Path> datasets;

    static {
        Storage.mapper.findAndRegisterModules();
    }

    private Storage() {
        this.models = new HashMap<>();
        this.datasets = new HashMap<>();
    }

    public static Storage get() {
        if (Storage.instance == null) {
            Storage.instance = new Storage();
        }

        return Storage.instance;
    }

    public List<Metadata> models() {
        return this.models.values().stream()
                .map(t -> {
                    try {
                        return readMetadata(t);
                    } catch (IOException e) {
                        // Silent Catch.
                        return null;
                    }
                })
                .filter(m -> m != null)
                .collect(Collectors.toList());
    }

    public List<Metadata> datasets() {
        return this.datasets.values().stream()
                .map(t -> {
                    try {
                        return readMetadata(t);
                    } catch (IOException e) {
                        // Silent Catch.
                        return null;
                    }
                })
                .filter(m -> m != null)
                .collect(Collectors.toList());
    }

    public Metadata save(MultipartFile file, String id, String owner, ObjectType type) throws IOException {
        Path root = type == ObjectType.MODEL ? Storage.modelDir : Storage.datasetDir;
        Path destDir = root.resolve(id);
        Metadata m = new Metadata(owner, id, destDir, type, LocalDateTime.now());

        switch (type) {
            case MODEL:
                Storage.saveToMemory(this.models, m, file);
                break;
            case DATASET:
                Storage.saveToMemory(this.datasets, m, file);
                break;
        }

        return m;
    }

    public void delete(String id, ObjectType type) throws IOException {
        switch (type) {
            case MODEL:
                Storage.removeFromMemory(this.models, id);
                break;
            case DATASET:
                Storage.removeFromMemory(this.datasets, id);
                break;
        }
    }

    public Metadata get(String id, ObjectType type) {
        HashMap<String, Path> objHashMap = type == ObjectType.MODEL ? this.models : this.datasets;

        if (!objHashMap.containsKey(id)) {
            return null;
        }

        Metadata m = null;
        Path target = objHashMap.get(id);

        for (int i = 0; i < 5; i++) {
            try {
                m = Storage.readMetadata(target);
                break;
            } catch (Exception e) {
                // Silent catch.
            }
        }

        return m;
    }

    private static Metadata readMetadata(Path root) throws StreamReadException, DatabindException, IOException {
        return Storage.mapper.readValue(root.resolve("metadata.json").toFile(),
                Metadata.class);
    }

    private static void saveToMemory(HashMap<String, Path> objectMap,
            Metadata m,
            MultipartFile f) throws IOException {
        if (objectMap.containsKey(m.getId())) {
            System.out.println(m.getId());
            System.out.println(objectMap.toString());
            throw new IOException();
        }

        Path destDir = m.getObjectPath();

        try {
            destDir.toFile().mkdirs();

            Path modelPath = destDir.resolve("artifact.zip");
            f.transferTo(modelPath);

            Path metadataPath = destDir.resolve("metadata.json");
            String metadataJson = Storage.mapper.writer(Storage.printer).writeValueAsString(m);
            FileUtils.writeStringToFile(metadataPath.toFile(),
                    metadataJson,
                    "UTF-8",
                    false);
        } catch (Exception e) {
            // Garantir que limpamos resquícios
            FileUtils.deleteDirectory(destDir.toFile());
            throw e;
        }

        objectMap.put(m.getId(), destDir);
    }

    private static void removeFromMemory(HashMap<String, Path> objectMap, String id) throws IOException {
        if (!objectMap.containsKey(id)) {
            throw new IOException();
        }

        Path destDir = objectMap.get(id);
        FileUtils.deleteDirectory(destDir.toFile());
        objectMap.remove(id);
    }
}
