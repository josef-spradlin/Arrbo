package arrbo.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "top_usage_players")
public class TopUsagePlayer {

  @Id
  @Column(name = "team_id")
  private Integer teamId;

  @Column(name = "player1_name")
  private String player1Name;

  @Column(name = "player1_usage")
  private Double player1Usage;

  @Column(name = "player2_name")
  private String player2Name;

  @Column(name = "player2_usage")
  private Double player2Usage;

  public Integer getTeamId() { return teamId; }
  public void setTeamId(Integer teamId) { this.teamId = teamId; }

  public String getPlayer1Name() { return player1Name; }
  public void setPlayer1Name(String player1Name) { this.player1Name = player1Name; }

  public Double getPlayer1Usage() { return player1Usage; }
  public void setPlayer1Usage(Double player1Usage) { this.player1Usage = player1Usage; }

  public String getPlayer2Name() { return player2Name; }
  public void setPlayer2Name(String player2Name) { this.player2Name = player2Name; }

  public Double getPlayer2Usage() { return player2Usage; }
  public void setPlayer2Usage(Double player2Usage) { this.player2Usage = player2Usage; }
}
