package arrbo.controller;

import arrbo.model.DefensiveEfficiency;
import arrbo.repo.DefensiveEfficiencyRepository;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DefenseController {

  private final DefensiveEfficiencyRepository repo;

  public DefenseController(DefensiveEfficiencyRepository repo) {
    this.repo = repo;
  }

  @GetMapping("/api/defense/efficiency")
  public List<DefensiveEfficiency> getDefensiveEfficiency() {
    return repo.findAll();
  }
}
