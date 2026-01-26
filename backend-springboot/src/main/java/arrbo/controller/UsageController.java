package arrbo.controller;

import arrbo.model.TopUsagePlayer;
import arrbo.repo.TopUsagePlayerRepository;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UsageController {

  private final TopUsagePlayerRepository repo;

  public UsageController(TopUsagePlayerRepository repo) {
    this.repo = repo;
  }

  @GetMapping("/api/usage/top")
  public List<TopUsagePlayer> getTopUsage() {
    return repo.findAll();
  }
}
