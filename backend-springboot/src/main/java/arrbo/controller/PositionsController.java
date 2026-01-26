package arrbo.controller;

import arrbo.model.Position;
import arrbo.repo.PositionRepository;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PositionsController {

  private final PositionRepository repo;

  public PositionsController(PositionRepository repo) {
    this.repo = repo;
  }

  @GetMapping("/api/positions")
  public List<Position> getPositions() {
    return repo.findAll();
  }
}
