package arrbo.controller;

import arrbo.model.Average;
import arrbo.repo.AverageRepository;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AveragesController {

  private final AverageRepository repo;

  public AveragesController(AverageRepository repo) {
    this.repo = repo;
  }

  @GetMapping("/api/averages")
  public List<Average> getAverages() {
    return repo.findAll();
  }
}
