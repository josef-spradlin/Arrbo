package arrbo.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import com.fasterxml.jackson.annotation.JsonProperty;

@Entity
@Table(name = "defensive_efficiency")
public class DefensiveEfficiency {

  @Id
  @Column(name = "team_id")
  private Integer teamId;

  @Column(name = "pg_efficiency")
  private Double pgEfficiency;

  @Column(name = "sg_efficiency")
  private Double sgEfficiency;

  @Column(name = "sf_efficiency")
  private Double sfEfficiency;

  @Column(name = "pf_efficiency")
  private Double pfEfficiency;

  @JsonProperty("cEfficiency") //Stabalize the name for this property
  @Column(name = "c_efficiency")
  private Double cEfficiency;

  public Integer getTeamId() { return teamId; }
  public void setTeamId(Integer teamId) { this.teamId = teamId; }

  public Double getPgEfficiency() { return pgEfficiency; }
  public void setPgEfficiency(Double pgEfficiency) { this.pgEfficiency = pgEfficiency; }

  public Double getSgEfficiency() { return sgEfficiency; }
  public void setSgEfficiency(Double sgEfficiency) { this.sgEfficiency = sgEfficiency; }

  public Double getSfEfficiency() { return sfEfficiency; }
  public void setSfEfficiency(Double sfEfficiency) { this.sfEfficiency = sfEfficiency; }

  public Double getPfEfficiency() { return pfEfficiency; }
  public void setPfEfficiency(Double pfEfficiency) { this.pfEfficiency = pfEfficiency; }

  public Double getCEfficiency() { return cEfficiency; }
  public void setCEfficiency(Double cEfficiency) { this.cEfficiency = cEfficiency; }
}
