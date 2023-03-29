package ai.mlhub.artifacts;

import java.nio.file.Path;
import java.time.LocalDateTime;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Metadata {

    @JsonProperty("owner")
    private String ownerUsername;

    @JsonProperty("id")
    private String id;

    @JsonProperty("path")
    private Path objectPath;

    @JsonProperty("type")
    private ObjectType type;

    @JsonProperty("date")
    private LocalDateTime creationDateTime;

    public String getOwnerUsername() {
        return this.ownerUsername;
    }

    public void setOwnerUsername(String ownerUsername) {
        this.ownerUsername = ownerUsername;
    }

    public String getId() {
        return this.id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Path getObjectPath() {
        return this.objectPath;
    }

    public void setObjectPath(Path objectPath) {
        this.objectPath = objectPath;
    }

    public ObjectType getType() {
        return this.type;
    }

    public void setType(ObjectType type) {
        this.type = type;
    }

    public LocalDateTime getCreationDateTime() {
        return this.creationDateTime;
    }

    public void setCreationDateTime(LocalDateTime creationDateTime) {
        this.creationDateTime = creationDateTime;
    }

    public Metadata(String ownerUsername, String id, Path objectPath, ObjectType type, LocalDateTime creationDateTime) {
        this.ownerUsername = ownerUsername;
        this.id = id;
        this.objectPath = objectPath;
        this.type = type;
        this.creationDateTime = creationDateTime;
    }

}
