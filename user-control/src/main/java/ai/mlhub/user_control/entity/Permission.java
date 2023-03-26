package ai.mlhub.user_control.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

/**
 * A classe {@link Permission} representa a tabela <b>permission</b> no Banco de
 * Dados.
 *
 * @author Moésio Filho
 * @version 1.0
 */
@Entity
@Table(name = "permission")
public class Permission {

    @Id
    @Column(name = "endpoint")
    private String endpoint;

    @Column(name = "description")
    private String description;

    @Column(name = "name")
    private String name;

    public String getEndpoint() {
        return this.endpoint;
    }

    public void setEndpoint(String endpoint) {
        this.endpoint = endpoint;
    }

    public String getDescription() {
        return this.description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

}
