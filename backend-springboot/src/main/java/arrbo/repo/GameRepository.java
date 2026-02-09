package arrbo.repo;

import arrbo.model.Game;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.time.LocalDate;
import java.util.List;

public interface GameRepository extends JpaRepository<Game, String> {
  List<Game> findByGameDateOrderByStartTimeUtcAsc(LocalDate gameDate);

  @Query("select max(g.gameDate) from Game g") 
  LocalDate findMaxGameDate();

  @Query(value = "select distinct to_char(game_date, 'YYYY-MM-DD') as d from games order by d asc", nativeQuery = true)
  List<String> findAvailableGameDateStringsAsc();
}
