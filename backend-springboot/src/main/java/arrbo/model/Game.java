package arrbo.model;

import jakarta.persistence.*;
import java.time.LocalDate;
import java.time.OffsetDateTime;

@Entity
@Table(name = "games")
public class Game {

  @Id
  @Column(name = "game_id")
  private String gameId;

  @Column(name = "game_date", nullable = false)
  private LocalDate gameDate;

  @Column(name = "start_time_utc")
  private OffsetDateTime startTimeUtc;

  @Column(name = "status_text")
  private String statusText;

  @Column(name = "home_team_id")
  private Integer homeTeamId;

  @Column(name = "home_team_abbr")
  private String homeTeamAbbr;

  @Column(name = "home_team_score")
  private Integer homeTeamScore;

  @Column(name = "away_team_id")
  private Integer awayTeamId;

  @Column(name = "away_team_abbr")
  private String awayTeamAbbr;

  @Column(name = "away_team_score")
  private Integer awayTeamScore;

  //getters/setters

  public String getGameId() {
    return gameId;
  }

  public void setGameId(String gameId) {
    this.gameId = gameId;
  }

  public LocalDate getGameDate() {
    return gameDate;
  }

  public void setGameDate(LocalDate gameDate) {
    this.gameDate = gameDate;
  }

  public OffsetDateTime getStartTimeUtc() {
    return startTimeUtc;
  }

  public void setStartTimeUtc(OffsetDateTime startTimeUtc) {
    this.startTimeUtc = startTimeUtc;
  }

  public String getStatusText() {
    return statusText;
  }

  public void setStatusText(String statusText) {
    this.statusText = statusText;
  }

  public Integer getHomeTeamId() {
    return homeTeamId;
  }

  public void setHomeTeamId(Integer homeTeamId) {
    this.homeTeamId = homeTeamId;
  }

  public String getHomeTeamAbbr() {
    return homeTeamAbbr;
  }

  public void setHomeTeamAbbr(String homeTeamAbbr) {
    this.homeTeamAbbr = homeTeamAbbr;
  }

  public Integer getHomeTeamScore() {
    return homeTeamScore;
  }

  public void setHomeTeamScore(Integer homeTeamScore) {
    this.homeTeamScore = homeTeamScore;
  }

  public Integer getAwayTeamId() {
    return awayTeamId;
  }

  public void setAwayTeamId(Integer awayTeamId) {
    this.awayTeamId = awayTeamId;
  }

  public String getAwayTeamAbbr() {
    return awayTeamAbbr;
  }

  public void setAwayTeamAbbr(String awayTeamAbbr) {
    this.awayTeamAbbr = awayTeamAbbr;
  }

  public Integer getAwayTeamScore() {
    return awayTeamScore;
  }

  public void setAwayTeamScore(Integer awayTeamScore) {
    this.awayTeamScore = awayTeamScore;
  }
}
