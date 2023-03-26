package ai.mlhub.user_control.repository;

import org.springframework.data.repository.CrudRepository;

import ai.mlhub.user_control.entity.Permission;

public interface PermissionRepository extends CrudRepository<Permission, String> {

}
