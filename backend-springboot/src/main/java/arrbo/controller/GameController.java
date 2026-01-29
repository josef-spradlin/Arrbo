package arrbo.controller;

import arrbo.model.Game;
import arrbo.repo.GameRepository;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("/api/games")
@CrossOrigin
public class GameController {

  private final GameRepository repo;

  public GameController(GameRepository repo) {
    this.repo = repo;
  }

  @GetMapping
  public List<Game> gamesByDate( //Format YYYY-MM-DD
      @RequestParam("date")
      @DateTimeFormat(iso = DateTimeFormat.ISO.DATE)
      LocalDate date
  ) {
    return repo.findByGameDateOrderByStartTimeUtcAsc(date);
  }

  @GetMapping("/{gameId}")
  public Game gameById(@PathVariable String gameId) {
    return repo.findById(gameId).orElseThrow(() -> new RuntimeException("Game not found: " + gameId));
  }

  
}
