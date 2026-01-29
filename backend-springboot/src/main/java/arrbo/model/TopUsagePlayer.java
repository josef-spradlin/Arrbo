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

   @Column(name = "player3_name")
  private String player3Name;

  @Column(name = "player3_usage") 
  private Double player3Usage;

  @Column(name = "player4_name")
  private String player4Name; 

  @Column(name = "player4_usage")
  private Double player4Usage;  

  @Column(name = "player5_name")
  private String player5Name;

  @Column(name = "player5_usage")
  private Double player5Usage;


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

  public String getPlayer3Name() { return player3Name; }
  public void setPlayer3Name(String player3Name) { this.player3Name = player3Name; }

  public Double getPlayer3Usage() { return player3Usage; }
  public void setPlayer3Usage(Double player3Usage) { this.player3Usage = player3Usage; }  

  public String getPlayer4Name() { return player4Name; }
  public void setPlayer4Name(String player4Name) { this.player4Name = player4Name; }

  public Double getPlayer4Usage() { return player4Usage; }
  public void setPlayer4Usage(Double player4Usage) { this.player4Usage = player4Usage; }

  public String getPlayer5Name() { return player5Name; }
  public void setPlayer5Name(String player5Name) { this.player5Name = player5Name; }

  public Double getPlayer5Usage() { return player5Usage; }
  public void setPlayer5Usage(Double player5Usage) { this.player5Usage = player5Usage; }
  
}
