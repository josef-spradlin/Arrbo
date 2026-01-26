package arrbo.model;

import jakarta.persistence.*;

@Entity
@Table(name = "averages")
public class Average {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Integer id;

  @Column(name = "player_name")
  private String playerName;

  @Column(name = "player_pts")
  private Double playerPts;

  @Column(name = "player_reb")
  private Double playerReb;

  @Column(name = "player_ast")
  private Double playerAst;

  @Column(name = "player_pra")
  private Double playerPra;

  public Integer getId() { return id; }
  public void setId(Integer id) { this.id = id; }

  public String getPlayerName() { return playerName; }
  public void setPlayerName(String playerName) { this.playerName = playerName; }

  public Double getPlayerPts() { return playerPts; }
  public void setPlayerPts(Double playerPts) { this.playerPts = playerPts; }

  public Double getPlayerReb() { return playerReb; }
  public void setPlayerReb(Double playerReb) { this.playerReb = playerReb; }

  public Double getPlayerAst() { return playerAst; }
  public void setPlayerAst(Double playerAst) { this.playerAst = playerAst; }

  public Double getPlayerPra() { return playerPra; }
  public void setPlayerPra(Double playerPra) { this.playerPra = playerPra; }
}
