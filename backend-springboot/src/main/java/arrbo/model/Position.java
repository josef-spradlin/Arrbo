package arrbo.model;

import jakarta.persistence.*;

@Entity
@Table(name = "positions")
public class Position {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Integer id;

  @Column(name = "player_name")
  private String playerName;

  @Column(name = "player_position")
  private String playerPosition;

  public Integer getId() { return id; }
  public void setId(Integer id) { this.id = id; }

  public String getPlayerName() { return playerName; }
  public void setPlayerName(String playerName) { this.playerName = playerName; }

  public String getPlayerPosition() { return playerPosition; }
  public void setPlayerPosition(String playerPosition) { this.playerPosition = playerPosition; }
}
