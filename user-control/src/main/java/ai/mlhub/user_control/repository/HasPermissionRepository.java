package ai.mlhub.user_control.repository;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

import ai.mlhub.user_control.entity.HasPermission;

public interface HasPermissionRepository extends CrudRepository<HasPermission, HasPermission.Key> {

    @Query("SELECT p FROM HasPermission p WHERE "
            + "p.username = :username")
    Iterable<HasPermission> getUserPermissions(String username);

}
