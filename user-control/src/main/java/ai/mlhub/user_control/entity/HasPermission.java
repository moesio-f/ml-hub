package ai.mlhub.user_control.entity;

import java.io.Serializable;
import java.util.Objects;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.IdClass;
import jakarta.persistence.Table;

/**
 * A classe {@link HasPermission} representa a tabela <b>has_permission</b> no
 * Banco de Dados.
 *
 * @author Moésio Filho
 * @version 1.0
 */
@Entity
@IdClass(HasPermission.Key.class)
@Table(name = "has_permission")
public class HasPermission {

    @Id
    @Column(name = "username")
    private String username;

    @Id
    @Column(name = "endpoint")
    private String endpoint;


    public String getUsername() {
        return this.username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEndpoint() {
        return this.endpoint;
    }

    public void setEndpoint(String endpoint) {
        this.endpoint = endpoint;
    }

    public static class Key implements Serializable {

        private String username;
        private String endpoint;

        @Override
        public boolean equals(Object o) {
            if (this == o) {
                return true;
            }
            if (o == null || getClass() != o.getClass()) {
                return false;
            }
            Key key = (Key) o;
            return (this.username == key.username) &&
                    (this.endpoint == key.endpoint);
        }

        @Override
        public int hashCode() {
            return Objects.hash(this.username, this.endpoint);
        }
    }

}
