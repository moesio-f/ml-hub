package ai.mlhub.user_control.repository;

import org.springframework.data.repository.CrudRepository;

import ai.mlhub.user_control.entity.User;

public interface UserRepository extends CrudRepository<User, String> {

}
