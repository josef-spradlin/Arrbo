package arrbo.repo;

import arrbo.model.Game;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDate;
import java.util.List;

public interface GameRepository extends JpaRepository<Game, String> {
  List<Game> findByGameDateOrderByStartTimeUtcAsc(LocalDate gameDate);
}
