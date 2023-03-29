package ai.mlhub.artifacts;

import java.io.IOException;
import java.util.Map;
import java.util.stream.Collectors;

import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

/**
 * Controlador da API.
 * 
 * <p>
 * Referências:
 * </p>
 * <p>
 * https://spring.io/guides/gs/uploading-files/
 * </p>
 * <p>
 * https://medium.com/@mertbozkurt84/spring-boot-upload-download-files-7ce6e8a3d277
 * </p>
 * 
 * @version 0.1
 */
@RestController
@RequestMapping(path = "/artifacts")
@CrossOrigin
public class MainController {

    private Storage storage = Storage.get();

    @GetMapping(path = "/models")
    public ResponseEntity<?> listModels() {
        return ResponseEntity.ok(this.storage.models()
                .stream()
                .map(MetadataResponse::fromMetadata)
                .collect(Collectors.toList()));
    }

    @GetMapping(path = "/datasets")
    public ResponseEntity<?> listDatasets() {
        return ResponseEntity.ok(this.storage.datasets()
                .stream()
                .map(MetadataResponse::fromMetadata)
                .collect(Collectors.toList()));
    }

    @GetMapping(path = "/metadata/model/{model}")
    public ResponseEntity<?> getModelMetadata(@PathVariable("model") String model) {

        Metadata obj = this.storage.get(model, ObjectType.MODEL);

        if (obj == null) {
            return ResponseEntity.badRequest().body(Map.of("msg", "Modelo não encontrado."));
        }

        return ResponseEntity.ok(MetadataResponse.fromMetadata(obj));
    }

    @GetMapping(path = "/metadata/dataset/{dataset}")
    public ResponseEntity<?> getDatasetMetadata(@PathVariable("dataset") String dataset) {

        Metadata obj = this.storage.get(dataset, ObjectType.DATASET);

        if (obj == null) {
            return ResponseEntity.badRequest().body(Map.of("msg", "Dataset não encontrado."));
        }

        return ResponseEntity.ok(MetadataResponse.fromMetadata(obj));
    }

    @GetMapping(path = "/download/model/{model}")
    @ResponseBody
    public ResponseEntity<?> getModel(@PathVariable("model") String model) {
        Metadata obj = this.storage.get(model, ObjectType.MODEL);

        if (obj == null) {
            return ResponseEntity.badRequest().body(Map.of("msg", "Modelo não encontrado."));
        }

        Resource resource = new FileSystemResource(obj.getObjectPath().resolve("artifact.zip"));

        return ResponseEntity
                .ok()
                .header(HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=\"" + obj.getId() + ".zip\"")
                .contentType(MediaType.parseMediaType("application/zip"))
                .body(resource);
    }

    @GetMapping(path = "/download/dataset/{dataset}")
    @ResponseBody
    public ResponseEntity<?> getDataset(@PathVariable("dataset") String dataset) {
        Metadata obj = this.storage.get(dataset, ObjectType.DATASET);

        if (obj == null) {
            return ResponseEntity.badRequest().body(Map.of("msg", "Dataset não encontrado."));
        }

        Resource resource = new FileSystemResource(obj.getObjectPath());

        return ResponseEntity
                .ok()
                .header(HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=\"" + obj.getId() + ".zip\"")
                .contentType(MediaType.parseMediaType("application/zip"))
                .body(resource);
    }

    @PostMapping(path = "/save/model/{owner}/{model}")
    public ResponseEntity<?> saveModel(@PathVariable("model") String model,
            @PathVariable("owner") String username,
            @RequestParam("file") MultipartFile file,
            RedirectAttributes redirectAttributes) {

        Metadata metadata = null;

        try {
            metadata = this.storage.save(file, model, username, ObjectType.MODEL);
        } catch (IOException e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError().build();
        }

        return ResponseEntity.ok(new SaveResponse(metadata));
    }

    @PostMapping(path = "/save/dataset/{owner}/{dataset}")
    public ResponseEntity<?> saveDataset(@PathVariable("dataset") String dataset,
            @PathVariable("owner") String username,
            @RequestParam("file") MultipartFile file,
            RedirectAttributes redirectAttributes) {
        Metadata metadata = null;

        try {
            metadata = this.storage.save(file, dataset, username, ObjectType.DATASET);
        } catch (IOException e) {
            return ResponseEntity.internalServerError().build();
        }

        return ResponseEntity.ok(new SaveResponse(metadata));
    }

    @DeleteMapping(path = "/delete/model/{model}")
    public ResponseEntity<?> deleteModel(@PathVariable("model") String model) {
        try {
            this.storage.delete(model, ObjectType.MODEL);
        } catch (IOException e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError().build();
        }

        return ResponseEntity.ok().build();
    }

    @DeleteMapping(path = "/delete/dataset/{dataset}")
    public ResponseEntity<?> deleteDataset(@PathVariable("dataset") String dataset) {
        try {
            this.storage.delete(dataset, ObjectType.DATASET);
        } catch (IOException e) {
            return ResponseEntity.internalServerError().build();
        }

        return ResponseEntity.ok().build();
    }


    private static class MetadataResponse {
        public String objectId;
        public String objectType;
        public String owner;

        public static MetadataResponse fromMetadata(Metadata m) {
            MetadataResponse r = new MetadataResponse();
            r.objectId = m.getId();
            r.objectType = m.getType() == ObjectType.MODEL ? "model" : "dataset";
            r.owner = m.getOwnerUsername();
            return r;
        }
    }

    private static class SaveResponse {
        public boolean success;
        public String objectType;
        public String objectId;

        public SaveResponse(Metadata metadata) {
            this.success = objectId == null;
            this.objectType = metadata.getType() == ObjectType.MODEL ? "model" : "dataset";
            this.objectId = metadata.getId();
        }

    }

}
