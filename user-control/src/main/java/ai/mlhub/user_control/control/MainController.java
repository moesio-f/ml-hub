package ai.mlhub.user_control.control;

import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.transaction.TransactionStatus;
import org.springframework.transaction.support.TransactionCallback;
import org.springframework.transaction.support.TransactionTemplate;
import org.springframework.web.bind.annotation.*;

import ai.mlhub.user_control.entity.User;
import ai.mlhub.user_control.entity.HasPermission;
import ai.mlhub.user_control.repository.HasPermissionRepository;
import ai.mlhub.user_control.repository.UserRepository;

/**
 * Controlador da API.
 * 
 * Referência:
 * https://www.oracle.com/br/technical-resources/articles/dsl/crud-rest-sb2-hibernate.html
 *
 * @version 0.1
 */
@RestController
@RequestMapping(path = "/user-control")
@CrossOrigin
public class MainController {

    @Autowired
    private UserRepository userRepo;

    @Autowired
    private HasPermissionRepository hasPermissionRepo;

    @Autowired
    private TransactionTemplate transactionTemplate;

    @GetMapping(path = "/list")
    public ResponseEntity<?> list() {
        return ResponseEntity.ok(this.userRepo.findAll());
    }

    @GetMapping(path = "/get/{username}")
    public ResponseEntity<?> get(@PathVariable("username") String username) {
        User u = this.userRepo.findById(username).orElse(null);

        if (u == null) {
            return ResponseEntity.notFound().build();
        }

        Iterable<HasPermission> permissions = this.hasPermissionRepo.getUserPermissions(username);
        List<String> p = StreamSupport.stream(permissions.spliterator(), false)
                .map(perm -> perm.getEndpoint()).collect(Collectors.toList());

        return ResponseEntity.ok(new ExtendedUser(u, p));
    }

    @PostMapping(path = "/create")
    public ResponseEntity<?> create(@RequestBody ExtendedUser user) {
        return this.transactionTemplate.execute(new TransactionCallback<ResponseEntity<?>>() {
            @Override
            public ResponseEntity<?> doInTransaction(TransactionStatus status) {
                User u = user.user;

                if (userRepo.findById(u.getUsername()).isPresent()) {
                    return ResponseEntity.badRequest().build();
                }

                u = userRepo.save(u);

                for (String endpoint : user.permissions) {
                    HasPermission p = new HasPermission();
                    p.setEndpoint(endpoint);
                    p.setUsername(u.getUsername());
                    hasPermissionRepo.save(p);
                }

                return ResponseEntity.ok(user);
            }
        });
    }

    @DeleteMapping(path = "/delete/{username}")
    public ResponseEntity<?> delete(@PathVariable("username") String username) {
        return this.transactionTemplate.execute(new TransactionCallback<ResponseEntity<?>>() {
            @Override
            public ResponseEntity<?> doInTransaction(TransactionStatus status) {
                User u = userRepo.findById(username).orElse(null);

                if (u == null) {
                    return ResponseEntity.notFound().build();
                }

                userRepo.delete(u);

                return ResponseEntity.ok().build();
            }
        });
    }

    @PutMapping(path = "/update/{username}")
    public ResponseEntity<?> update(@PathVariable("username") String username,
            @RequestBody ExtendedUser updated) {
        return this.transactionTemplate.execute(new TransactionCallback<ResponseEntity<?>>() {
            @Override
            public ResponseEntity<?> doInTransaction(TransactionStatus status) {
                User u = userRepo.findById(username).orElse(null);
                User newUser = updated.user;

                if (u == null) {
                    return ResponseEntity.notFound().build();
                } else if (!u.getUsername().equals(newUser.getUsername())) {
                    return ResponseEntity.badRequest().build();
                }

                // Atualizações dos dados
                u.setName(newUser.getName());
                u.setNotes(newUser.getNotes());
                u.setPassword(newUser.getPassword());
                u.setRegistrationDate(newUser.getRegistrationDate());
                u.setType(newUser.getType());

                // Salvando resultados
                userRepo.save(u);

                // Atualização nas permissões
                List<String> extraPermissions = StreamSupport
                        .stream(hasPermissionRepo.getUserPermissions(username).spliterator(), false)
                        .map(hp -> hp.getEndpoint())
                        .filter(e -> !updated.permissions.contains(e))
                        .collect(Collectors.toList());

                for (String endpoint : extraPermissions) {
                    HasPermission p = new HasPermission();
                    p.setEndpoint(endpoint);
                    p.setUsername(u.getUsername());
                    hasPermissionRepo.save(p);
                }

                return ResponseEntity.ok().build();
            }
        });
    }

    /**
     * Essa classe representa uma versão "estendida" de um usuário,
     * onde a separação interna do Banco de Dados (permissões e usuários)
     * são mescladas, expondo apenas uma entidade única.
     */
    private static class ExtendedUser {
        public User user;
        public List<String> permissions;

        public ExtendedUser(User u, List<String> p) {
            this.user = u;
            this.permissions = p;
        }
    }

}
