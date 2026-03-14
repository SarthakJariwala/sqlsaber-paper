Thread: d6d53fba-1f6c-41ea-82dd-2ad1c1af694a

Database: european_football_2
Title: List the long name of teams with above-average build-up play passing in 2012.

Context: long name of teams refers to team_long_name; build-up play passing refers to buildUpPlayPassing; above-average build-up play passing = buildUpPlayPassing > DIVIDE(SUM(buildUpPlayPassing), COUNT(team_long_name) WHERE 
buildUpPlayPassing IS NOT NULL); in 2012 refers to strftime('%Y', date) = '2012'; 
Last activity: 2026-03-11 19:44:02
Model: gemini-3.1-pro-preview

**User:**

List the long name of teams with above-average build-up play passing in 2012.

Context: long name of teams refers to team_long_name; build-up play passing refers to buildUpPlayPassing; above-average build-up play passing = buildUpPlayPassing > DIVIDE(SUM(buildUpPlayPassing), COUNT(team_long_name) WHERE 
buildUpPlayPassing IS NOT NULL); in 2012 refers to strftime('%Y', date) = '2012'; 


**🔎 Searching knowledge base**

- **query**: team_long_name buildUpPlayPassing

*No results*


**⚙️ Discovering available tables**

**Database Tables (7 total)**

| Schema   | Table Name        | Type   |
|----------|-------------------|--------|
| main     | Country           | table  |
| main     | League            | table  |
| main     | Match             | table  |
| main     | Player            | table  |
| main     | Player_Attributes | table  |
| main     | Team              | table  |
| main     | Team_Attributes   | table  |


**⚙️ Examining schema**


**Schema Information (2 tables):**

**Table: main.Team**

| Column           | Type    | Nullable   | Default   | Comments   |
|------------------|---------|------------|-----------|------------|
| id               | INTEGER | True       |           |            |
| team_api_id      | INTEGER | True       |           |            |
| team_fifa_api_id | INTEGER | True       |           |            |
| team_long_name   | TEXT    | True       |           |            |
| team_short_name  | TEXT    | True       |           |            |

**Primary Keys:** id

**Table: main.Team_Attributes**

| Column                         | Type    | Nullable   | Default   | Comments   |
|--------------------------------|---------|------------|-----------|------------|
| id                             | INTEGER | True       |           |            |
| team_fifa_api_id               | INTEGER | True       |           |            |
| team_api_id                    | INTEGER | True       |           |            |
| date                           | TEXT    | True       |           |            |
| buildUpPlaySpeed               | INTEGER | True       |           |            |
| buildUpPlaySpeedClass          | TEXT    | True       |           |            |
| buildUpPlayDribbling           | INTEGER | True       |           |            |
| buildUpPlayDribblingClass      | TEXT    | True       |           |            |
| buildUpPlayPassing             | INTEGER | True       |           |            |
| buildUpPlayPassingClass        | TEXT    | True       |           |            |
| buildUpPlayPositioningClass    | TEXT    | True       |           |            |
| chanceCreationPassing          | INTEGER | True       |           |            |
| chanceCreationPassingClass     | TEXT    | True       |           |            |
| chanceCreationCrossing         | INTEGER | True       |           |            |
| chanceCreationCrossingClass    | TEXT    | True       |           |            |
| chanceCreationShooting         | INTEGER | True       |           |            |
| chanceCreationShootingClass    | TEXT    | True       |           |            |
| chanceCreationPositioningClass | TEXT    | True       |           |            |
| defencePressure                | INTEGER | True       |           |            |
| defencePressureClass           | TEXT    | True       |           |            |
| defenceAggression              | INTEGER | True       |           |            |
| defenceAggressionClass         | TEXT    | True       |           |            |
| defenceTeamWidth               | INTEGER | True       |           |            |
| defenceTeamWidthClass          | TEXT    | True       |           |            |
| defenceDefenderLineClass       | TEXT    | True       |           |            |

**Primary Keys:** id

**Foreign Keys:** team_api_id -> main.Team.team_api_id, team_fifa_api_id -> main.Team.team_fifa_api_id


**Executing SQL:**

```sql
SELECT T.team_long_name
FROM Team AS T
JOIN Team_Attributes AS TA
ON T.team_api_id = TA.team_api_id
WHERE strftime('%Y', TA.date) = '2012'
  AND TA.buildUpPlayPassing > (
    SELECT AVG(TA2.buildUpPlayPassing)
    FROM Team AS T2
    JOIN Team_Attributes AS TA2
    ON T2.team_api_id = TA2.team_api_id
    WHERE strftime('%Y', TA2.date) = '2012'
  )
```


**Results (129 rows):**

| team_long_name               |
|------------------------------|
| Aberdeen                     |
| AC Ajaccio                   |
| Milan                        |
| UD Almería                   |
| Angers SCO                   |
| Aston Villa                  |
| Atalanta                     |
| Athletic Club de Bilbao      |
| Atlético Madrid              |
| FC Augsburg                  |
| Bari                         |
| Bayer 04 Leverkusen          |
| Beerschot AC                 |
| Birmingham City              |
| Blackburn Rovers             |
| Blackpool                    |
| Bologna                      |
| Bolton Wanderers             |
| Borussia Mönchengladbach     |
| Stade Brestois 29            |
| SM Caen                      |
| Cagliari                     |
| Cardiff City                 |
| Catania                      |
| RC Celta de Vigo             |
| Celtic                       |
| KSV Cercle Brugge            |
| Chievo Verona                |
| Club Brugge KV               |
| Córdoba CF                   |
| Cracovia                     |
| Dundee United                |
| Dunfermline Athletic         |
| Eintracht Braunschweig       |
| Elche CF                     |
| Empoli                       |
| Everton                      |
| Excelsior                    |
| 1. FC Köln                   |
| FC Porto                     |
| FC Utrecht                   |
| Fiorentina                   |
| SC Freiburg                  |
| KRC Genk                     |
| Genoa                        |
| GKS Bełchatów                |
| Grasshopper Club Zürich      |
| Hannover 96                  |
| Heart of Midlothian          |
| Hércules Club de Fútbol      |
| TSG 1899 Hoffenheim          |
| Inter                        |
| Inverness Caledonian Thistle |
| Jagiellonia Białystok        |
| 1. FC Kaiserslautern         |
| Kilmarnock                   |
| Korona Kielce                |
| KV Mechelen                  |
| Lazio                        |
| Le Havre AC                  |
| Lecce                        |
| Lech Poznań                  |
| Lechia Gdańsk                |
| Legia Warszawa               |
| Levante UD                   |
| Lierse SK                    |
| Liverpool                    |
| Livorno                      |
| Widzew Łódź                  |
| Sporting Lokeren             |
| Olympique Lyonnais           |
| 1. FSV Mainz 05              |
| RCD Mallorca                 |
| Manchester City              |
| Manchester United            |
| Olympique de Marseille       |
| Middlesbrough                |
| RAEC Mons                    |
| Motherwell                   |
| FC Nantes                    |
| Newcastle United             |
| OGC Nice                     |
| Norwich City                 |
| Novara                       |
| CA Osasuna                   |
| Oud-Heverlee Leuven          |
| SC Paderborn 07              |
| Pescara                      |
| Podbeskidzie Bielsko-Biała   |
| Portsmouth                   |
| Queens Park Rangers          |
| RC Recreativo                |
| Reggio Calabria              |
| Siena                        |
| Roda JC Kerkrade             |
| Ruch Chorzów                 |
| AS Saint-Étienne             |
| Sassuolo                     |
| SC Bastia                    |
| SC Heerenveen                |
| Servette FC                  |
| Sevilla FC                   |
| Śląsk Wrocław                |
| Southampton                  |
| Sporting CP                  |
| Napoli                       |
| St. Mirren                   |
| FC St. Pauli                 |
| St. Johnstone FC             |
| Sint-Truidense VV            |
| Standard de Liège            |
| Stoke City                   |
| Sunderland                   |
| Torino                       |
| Toulouse FC                  |
| ES Troyes AC                 |
| Valenciennes FC              |
| Real Valladolid              |
| Hellas Verona                |
| VVV-Venlo                    |
| Watford                      |
| West Ham United              |
| KVC Westerlo                 |
| Widzew Łódź                  |
| VfL Wolfsburg                |
| Wolverhampton Wanderers      |
| Neuchâtel Xamax              |
| BSC Young Boys               |
| SV Zulte-Waregem             |


**Executing SQL:**

```sql
SELECT T.team_long_name 
FROM Team AS T 
JOIN Team_Attributes AS TA 
ON T.team_api_id = TA.team_api_id 
WHERE strftime('%Y', TA.date) = '2012' 
  AND TA.buildUpPlayPassing > (
    SELECT CAST(SUM(TA2.buildUpPlayPassing) AS REAL) / COUNT(T2.team_long_name)
    FROM Team AS T2 
    JOIN Team_Attributes AS TA2 
    ON T2.team_api_id = TA2.team_api_id 
    WHERE strftime('%Y', TA2.date) = '2012' 
      AND TA2.buildUpPlayPassing IS NOT NULL
  )
```


**Results (129 rows):**

| team_long_name               |
|------------------------------|
| Aberdeen                     |
| AC Ajaccio                   |
| Milan                        |
| UD Almería                   |
| Angers SCO                   |
| Aston Villa                  |
| Atalanta                     |
| Athletic Club de Bilbao      |
| Atlético Madrid              |
| FC Augsburg                  |
| Bari                         |
| Bayer 04 Leverkusen          |
| Beerschot AC                 |
| Birmingham City              |
| Blackburn Rovers             |
| Blackpool                    |
| Bologna                      |
| Bolton Wanderers             |
| Borussia Mönchengladbach     |
| Stade Brestois 29            |
| SM Caen                      |
| Cagliari                     |
| Cardiff City                 |
| Catania                      |
| RC Celta de Vigo             |
| Celtic                       |
| KSV Cercle Brugge            |
| Chievo Verona                |
| Club Brugge KV               |
| Córdoba CF                   |
| Cracovia                     |
| Dundee United                |
| Dunfermline Athletic         |
| Eintracht Braunschweig       |
| Elche CF                     |
| Empoli                       |
| Everton                      |
| Excelsior                    |
| 1. FC Köln                   |
| FC Porto                     |
| FC Utrecht                   |
| Fiorentina                   |
| SC Freiburg                  |
| KRC Genk                     |
| Genoa                        |
| GKS Bełchatów                |
| Grasshopper Club Zürich      |
| Hannover 96                  |
| Heart of Midlothian          |
| Hércules Club de Fútbol      |
| TSG 1899 Hoffenheim          |
| Inter                        |
| Inverness Caledonian Thistle |
| Jagiellonia Białystok        |
| 1. FC Kaiserslautern         |
| Kilmarnock                   |
| Korona Kielce                |
| KV Mechelen                  |
| Lazio                        |
| Le Havre AC                  |
| Lecce                        |
| Lech Poznań                  |
| Lechia Gdańsk                |
| Legia Warszawa               |
| Levante UD                   |
| Lierse SK                    |
| Liverpool                    |
| Livorno                      |
| Widzew Łódź                  |
| Sporting Lokeren             |
| Olympique Lyonnais           |
| 1. FSV Mainz 05              |
| RCD Mallorca                 |
| Manchester City              |
| Manchester United            |
| Olympique de Marseille       |
| Middlesbrough                |
| RAEC Mons                    |
| Motherwell                   |
| FC Nantes                    |
| Newcastle United             |
| OGC Nice                     |
| Norwich City                 |
| Novara                       |
| CA Osasuna                   |
| Oud-Heverlee Leuven          |
| SC Paderborn 07              |
| Pescara                      |
| Podbeskidzie Bielsko-Biała   |
| Portsmouth                   |
| Queens Park Rangers          |
| RC Recreativo                |
| Reggio Calabria              |
| Siena                        |
| Roda JC Kerkrade             |
| Ruch Chorzów                 |
| AS Saint-Étienne             |
| Sassuolo                     |
| SC Bastia                    |
| SC Heerenveen                |
| Servette FC                  |
| Sevilla FC                   |
| Śląsk Wrocław                |
| Southampton                  |
| Sporting CP                  |
| Napoli                       |
| St. Mirren                   |
| FC St. Pauli                 |
| St. Johnstone FC             |
| Sint-Truidense VV            |
| Standard de Liège            |
| Stoke City                   |
| Sunderland                   |
| Torino                       |
| Toulouse FC                  |
| ES Troyes AC                 |
| Valenciennes FC              |
| Real Valladolid              |
| Hellas Verona                |
| VVV-Venlo                    |
| Watford                      |
| West Ham United              |
| KVC Westerlo                 |
| Widzew Łódź                  |
| VfL Wolfsburg                |
| Wolverhampton Wanderers      |
| Neuchâtel Xamax              |
| BSC Young Boys               |
| SV Zulte-Waregem             |


**Executing SQL:**

```sql
SELECT Team.team_long_name, count(*) as cnt 
FROM Team 
JOIN Team_Attributes ON Team.team_api_id = Team_Attributes.team_api_id 
WHERE strftime('%Y', Team_Attributes.date) = '2012' 
GROUP BY Team.team_long_name 
ORDER BY cnt DESC LIMIT 5
```


**Results (5 rows):**

| team_long_name           |   cnt |
|--------------------------|-------|
| Widzew Łódź              |     2 |
| Śląsk Wrocław            |     1 |
| Évian Thonon Gaillard FC |     1 |
| Zagłębie Lubin           |     1 |
| Xerez Club Deportivo     |     1 |


**Executing SQL:**

```sql
SELECT DISTINCT Team.team_long_name
FROM Team
JOIN Team_Attributes
  ON Team.team_api_id = Team_Attributes.team_api_id
WHERE strftime('%Y', Team_Attributes.date) = '2012'
  AND Team_Attributes.buildUpPlayPassing > (
    SELECT CAST(SUM(Team_Attributes.buildUpPlayPassing) AS REAL) / COUNT(Team.team_long_name)
    FROM Team_Attributes
    JOIN Team
      ON Team_Attributes.team_api_id = Team.team_api_id
    WHERE Team_Attributes.buildUpPlayPassing IS NOT NULL
      AND strftime('%Y', Team_Attributes.date) = '2012'
  )
```


**Results (128 rows):**

| team_long_name               |
|------------------------------|
| Aberdeen                     |
| AC Ajaccio                   |
| Milan                        |
| UD Almería                   |
| Angers SCO                   |
| Aston Villa                  |
| Atalanta                     |
| Athletic Club de Bilbao      |
| Atlético Madrid              |
| FC Augsburg                  |
| Bari                         |
| Bayer 04 Leverkusen          |
| Beerschot AC                 |
| Birmingham City              |
| Blackburn Rovers             |
| Blackpool                    |
| Bologna                      |
| Bolton Wanderers             |
| Borussia Mönchengladbach     |
| Stade Brestois 29            |
| SM Caen                      |
| Cagliari                     |
| Cardiff City                 |
| Catania                      |
| RC Celta de Vigo             |
| Celtic                       |
| KSV Cercle Brugge            |
| Chievo Verona                |
| Club Brugge KV               |
| Córdoba CF                   |
| Cracovia                     |
| Dundee United                |
| Dunfermline Athletic         |
| Eintracht Braunschweig       |
| Elche CF                     |
| Empoli                       |
| Everton                      |
| Excelsior                    |
| 1. FC Köln                   |
| FC Porto                     |
| FC Utrecht                   |
| Fiorentina                   |
| SC Freiburg                  |
| KRC Genk                     |
| Genoa                        |
| GKS Bełchatów                |
| Grasshopper Club Zürich      |
| Hannover 96                  |
| Heart of Midlothian          |
| Hércules Club de Fútbol      |
| TSG 1899 Hoffenheim          |
| Inter                        |
| Inverness Caledonian Thistle |
| Jagiellonia Białystok        |
| 1. FC Kaiserslautern         |
| Kilmarnock                   |
| Korona Kielce                |
| KV Mechelen                  |
| Lazio                        |
| Le Havre AC                  |
| Lecce                        |
| Lech Poznań                  |
| Lechia Gdańsk                |
| Legia Warszawa               |
| Levante UD                   |
| Lierse SK                    |
| Liverpool                    |
| Livorno                      |
| Widzew Łódź                  |
| Sporting Lokeren             |
| Olympique Lyonnais           |
| 1. FSV Mainz 05              |
| RCD Mallorca                 |
| Manchester City              |
| Manchester United            |
| Olympique de Marseille       |
| Middlesbrough                |
| RAEC Mons                    |
| Motherwell                   |
| FC Nantes                    |
| Newcastle United             |
| OGC Nice                     |
| Norwich City                 |
| Novara                       |
| CA Osasuna                   |
| Oud-Heverlee Leuven          |
| SC Paderborn 07              |
| Pescara                      |
| Podbeskidzie Bielsko-Biała   |
| Portsmouth                   |
| Queens Park Rangers          |
| RC Recreativo                |
| Reggio Calabria              |
| Siena                        |
| Roda JC Kerkrade             |
| Ruch Chorzów                 |
| AS Saint-Étienne             |
| Sassuolo                     |
| SC Bastia                    |
| SC Heerenveen                |
| Servette FC                  |
| Sevilla FC                   |
| Śląsk Wrocław                |
| Southampton                  |
| Sporting CP                  |
| Napoli                       |
| St. Mirren                   |
| FC St. Pauli                 |
| St. Johnstone FC             |
| Sint-Truidense VV            |
| Standard de Liège            |
| Stoke City                   |
| Sunderland                   |
| Torino                       |
| Toulouse FC                  |
| ES Troyes AC                 |
| Valenciennes FC              |
| Real Valladolid              |
| Hellas Verona                |
| VVV-Venlo                    |
| Watford                      |
| West Ham United              |
| KVC Westerlo                 |
| VfL Wolfsburg                |
| Wolverhampton Wanderers      |
| Neuchâtel Xamax              |
| BSC Young Boys               |
| SV Zulte-Waregem             |


**Executing SQL:**

```sql
SELECT SUM(Team_Attributes.buildUpPlayPassing) / COUNT(Team.team_long_name), CAST(SUM(Team_Attributes.buildUpPlayPassing) AS REAL) / COUNT(Team.team_long_name), AVG(Team_Attributes.buildUpPlayPassing)
    FROM Team_Attributes
    JOIN Team
      ON Team_Attributes.team_api_id = Team.team_api_id
    WHERE Team_Attributes.buildUpPlayPassing IS NOT NULL
      AND strftime('%Y', Team_Attributes.date) = '2012'
```


**Results (1 rows):**

|   SUM(Team_Attributes.buildUpPlayPassing) / COUNT(Team.team_long_name) |   CAST(SUM(Team_Attributes.buildUpPlayPassing) AS REAL) / COUNT(Team.team_long_name) |   AVG(Team_Attributes.buildUpPlayPassing) |
|------------------------------------------------------------------------|--------------------------------------------------------------------------------------|-------------------------------------------|
|                                                                     49 |                                                                              49.3306 |                                   49.3306 |


**Executing SQL:**

```sql
SELECT SUM(Team_Attributes.buildUpPlayPassing) / COUNT(Team.team_long_name), CAST(SUM(Team_Attributes.buildUpPlayPassing) AS REAL) / COUNT(Team.team_long_name), AVG(Team_Attributes.buildUpPlayPassing)
    FROM Team_Attributes
    JOIN Team
      ON Team_Attributes.team_api_id = Team.team_api_id
    WHERE Team_Attributes.buildUpPlayPassing IS NOT NULL
```


**Results (1 rows):**

|   SUM(Team_Attributes.buildUpPlayPassing) / COUNT(Team.team_long_name) |   CAST(SUM(Team_Attributes.buildUpPlayPassing) AS REAL) / COUNT(Team.team_long_name) |   AVG(Team_Attributes.buildUpPlayPassing) |
|------------------------------------------------------------------------|--------------------------------------------------------------------------------------|-------------------------------------------|
|                                                                     48 |                                                                              48.4904 |                                   48.4904 |


**Executing SQL:**

```sql
SELECT T.team_long_name
FROM Team AS T
JOIN Team_Attributes AS TA
ON T.team_api_id = TA.team_api_id
WHERE strftime('%Y', TA.date) = '2012'
  AND TA.buildUpPlayPassing > (
    SELECT CAST(SUM(TA2.buildUpPlayPassing) AS REAL) / COUNT(T2.team_long_name)
    FROM Team AS T2
    JOIN Team_Attributes AS TA2
    ON T2.team_api_id = TA2.team_api_id
    WHERE TA2.buildUpPlayPassing IS NOT NULL
  );
```


**Results (137 rows):**

| team_long_name               |
|------------------------------|
| Aberdeen                     |
| AC Ajaccio                   |
| Milan                        |
| UD Almería                   |
| Angers SCO                   |
| Aston Villa                  |
| Atalanta                     |
| Athletic Club de Bilbao      |
| Atlético Madrid              |
| FC Augsburg                  |
| AJ Auxerre                   |
| Bari                         |
| Bayer 04 Leverkusen          |
| Beerschot AC                 |
| Birmingham City              |
| Blackburn Rovers             |
| Blackpool                    |
| Bologna                      |
| Bolton Wanderers             |
| Borussia Mönchengladbach     |
| Stade Brestois 29            |
| SM Caen                      |
| Cagliari                     |
| Cardiff City                 |
| Catania                      |
| RC Celta de Vigo             |
| Celtic                       |
| KSV Cercle Brugge            |
| Chievo Verona                |
| Club Brugge KV               |
| Córdoba CF                   |
| Cracovia                     |
| Dijon FCO                    |
| Dundee United                |
| Dunfermline Athletic         |
| Eintracht Braunschweig       |
| Elche CF                     |
| Empoli                       |
| Everton                      |
| Excelsior                    |
| 1. FC Köln                   |
| FC Porto                     |
| FC Utrecht                   |
| Fiorentina                   |
| SC Freiburg                  |
| KRC Genk                     |
| Genoa                        |
| GKS Bełchatów                |
| Grasshopper Club Zürich      |
| Hannover 96                  |
| Heart of Midlothian          |
| Hércules Club de Fútbol      |
| TSG 1899 Hoffenheim          |
| Inter                        |
| Inverness Caledonian Thistle |
| Jagiellonia Białystok        |
| 1. FC Kaiserslautern         |
| Kilmarnock                   |
| Korona Kielce                |
| KV Mechelen                  |
| FC Lausanne-Sports           |
| Lazio                        |
| Le Havre AC                  |
| Lecce                        |
| Lech Poznań                  |
| Lechia Gdańsk                |
| Legia Warszawa               |
| RC Lens                      |
| Levante UD                   |
| Lierse SK                    |
| Liverpool                    |
| Livorno                      |
| Widzew Łódź                  |
| Sporting Lokeren             |
| Olympique Lyonnais           |
| 1. FSV Mainz 05              |
| RCD Mallorca                 |
| Manchester City              |
| Manchester United            |
| Olympique de Marseille       |
| FC Metz                      |
| Middlesbrough                |
| RAEC Mons                    |
| Motherwell                   |
| AS Nancy-Lorraine            |
| FC Nantes                    |
| Newcastle United             |
| OGC Nice                     |
| Norwich City                 |
| Novara                       |
| 1. FC Nürnberg               |
| CA Osasuna                   |
| Oud-Heverlee Leuven          |
| SC Paderborn 07              |
| Pescara                      |
| Podbeskidzie Bielsko-Biała   |
| Portsmouth                   |
| Queens Park Rangers          |
| Reading                      |
| RC Recreativo                |
| Reggio Calabria              |
| Siena                        |
| Roda JC Kerkrade             |
| Ruch Chorzów                 |
| AS Saint-Étienne             |
| Sassuolo                     |
| SC Bastia                    |
| SC Heerenveen                |
| Servette FC                  |
| Sevilla FC                   |
| Śląsk Wrocław                |
| Southampton                  |
| Sporting CP                  |
| Napoli                       |
| St. Mirren                   |
| FC St. Pauli                 |
| St. Johnstone FC             |
| Sint-Truidense VV            |
| Standard de Liège            |
| Stoke City                   |
| Sunderland                   |
| Torino                       |
| Toulouse FC                  |
| ES Troyes AC                 |
| Valenciennes FC              |
| Real Valladolid              |
| Hellas Verona                |
| VVV-Venlo                    |
| Watford                      |
| West Ham United              |
| KVC Westerlo                 |
| Widzew Łódź                  |
| VfL Wolfsburg                |
| Wolverhampton Wanderers      |
| Neuchâtel Xamax              |
| BSC Young Boys               |
| SV Zulte-Waregem             |


**Executing SQL:**

```sql
SELECT Team.team_long_name
FROM Team
JOIN Team_Attributes ON Team.team_api_id = Team_Attributes.team_api_id
WHERE strftime('%Y', Team_Attributes.date) = '2012' 
  AND Team_Attributes.buildUpPlayPassing > (
    SELECT SUM(Team_Attributes.buildUpPlayPassing) * 1.0 / COUNT(Team.team_long_name)
    FROM Team
    JOIN Team_Attributes ON Team.team_api_id = Team_Attributes.team_api_id
    WHERE Team_Attributes.buildUpPlayPassing IS NOT NULL
  )
```


**Results (137 rows):**

| team_long_name               |
|------------------------------|
| Aberdeen                     |
| AC Ajaccio                   |
| Milan                        |
| UD Almería                   |
| Angers SCO                   |
| Aston Villa                  |
| Atalanta                     |
| Athletic Club de Bilbao      |
| Atlético Madrid              |
| FC Augsburg                  |
| AJ Auxerre                   |
| Bari                         |
| Bayer 04 Leverkusen          |
| Beerschot AC                 |
| Birmingham City              |
| Blackburn Rovers             |
| Blackpool                    |
| Bologna                      |
| Bolton Wanderers             |
| Borussia Mönchengladbach     |
| Stade Brestois 29            |
| SM Caen                      |
| Cagliari                     |
| Cardiff City                 |
| Catania                      |
| RC Celta de Vigo             |
| Celtic                       |
| KSV Cercle Brugge            |
| Chievo Verona                |
| Club Brugge KV               |
| Córdoba CF                   |
| Cracovia                     |
| Dijon FCO                    |
| Dundee United                |
| Dunfermline Athletic         |
| Eintracht Braunschweig       |
| Elche CF                     |
| Empoli                       |
| Everton                      |
| Excelsior                    |
| 1. FC Köln                   |
| FC Porto                     |
| FC Utrecht                   |
| Fiorentina                   |
| SC Freiburg                  |
| KRC Genk                     |
| Genoa                        |
| GKS Bełchatów                |
| Grasshopper Club Zürich      |
| Hannover 96                  |
| Heart of Midlothian          |
| Hércules Club de Fútbol      |
| TSG 1899 Hoffenheim          |
| Inter                        |
| Inverness Caledonian Thistle |
| Jagiellonia Białystok        |
| 1. FC Kaiserslautern         |
| Kilmarnock                   |
| Korona Kielce                |
| KV Mechelen                  |
| FC Lausanne-Sports           |
| Lazio                        |
| Le Havre AC                  |
| Lecce                        |
| Lech Poznań                  |
| Lechia Gdańsk                |
| Legia Warszawa               |
| RC Lens                      |
| Levante UD                   |
| Lierse SK                    |
| Liverpool                    |
| Livorno                      |
| Widzew Łódź                  |
| Sporting Lokeren             |
| Olympique Lyonnais           |
| 1. FSV Mainz 05              |
| RCD Mallorca                 |
| Manchester City              |
| Manchester United            |
| Olympique de Marseille       |
| FC Metz                      |
| Middlesbrough                |
| RAEC Mons                    |
| Motherwell                   |
| AS Nancy-Lorraine            |
| FC Nantes                    |
| Newcastle United             |
| OGC Nice                     |
| Norwich City                 |
| Novara                       |
| 1. FC Nürnberg               |
| CA Osasuna                   |
| Oud-Heverlee Leuven          |
| SC Paderborn 07              |
| Pescara                      |
| Podbeskidzie Bielsko-Biała   |
| Portsmouth                   |
| Queens Park Rangers          |
| Reading                      |
| RC Recreativo                |
| Reggio Calabria              |
| Siena                        |
| Roda JC Kerkrade             |
| Ruch Chorzów                 |
| AS Saint-Étienne             |
| Sassuolo                     |
| SC Bastia                    |
| SC Heerenveen                |
| Servette FC                  |
| Sevilla FC                   |
| Śląsk Wrocław                |
| Southampton                  |
| Sporting CP                  |
| Napoli                       |
| St. Mirren                   |
| FC St. Pauli                 |
| St. Johnstone FC             |
| Sint-Truidense VV            |
| Standard de Liège            |
| Stoke City                   |
| Sunderland                   |
| Torino                       |
| Toulouse FC                  |
| ES Troyes AC                 |
| Valenciennes FC              |
| Real Valladolid              |
| Hellas Verona                |
| VVV-Venlo                    |
| Watford                      |
| West Ham United              |
| KVC Westerlo                 |
| Widzew Łódź                  |
| VfL Wolfsburg                |
| Wolverhampton Wanderers      |
| Neuchâtel Xamax              |
| BSC Young Boys               |
| SV Zulte-Waregem             |

**Assistant:**

<analysis>
To solve this request, we need to find the names of teams whose `buildUpPlayPassing` score in 2012 was higher than the average `buildUpPlayPassing` score.

1. **Understand the Tables**: 
   - `Team`: Contains information like the team's long name (`team_long_name`).
   - `Team_Attributes`: Contains performance attributes recorded over various dates, specifically `buildUpPlayPassing` and `date`.

2. **Map the Entities & Relationships**:
   - `team_long_name` corresponds to `Team.team_long_name`.
   - `build-up play passing` corresponds to `Team_Attributes.buildUpPlayPassing`.
   - The tables can be joined via `team_api_id`.

3. **Incorporate the Context**:
   - The condition "in 2012" uses `strftime('%Y', date) = '2012'`.
   - "Above-average" is defined by checking if the team's attribute score is greater than the total sum of `buildUpPlayPassing` divided by the total count of valid entries (`COUNT(team_long_name)`). 

4. **Construct the Query**:
   - Start by joining `Team` and `Team_Attributes` to get the team names alongside their scores in 2012.
   - For the above-average filter, use a subquery to compute the average over all records where `buildUpPlayPassing IS NOT NULL`. Following the context formula `DIVIDE(SUM(...), COUNT(...))`, we will divide the sum of passing scores by the 
count of team names. I'll cast the sum as a floating-point number (`REAL`) so the result retains decimal precision rather than integer truncation.
</analysis>

Here is the SQL query to find the requested team names:

```sql
SELECT Team.team_long_name
FROM Team
JOIN Team_Attributes
  ON Team.team_api_id = Team_Attributes.team_api_id
WHERE strftime('%Y', Team_Attributes.date) = '2012'
  AND Team_Attributes.buildUpPlayPassing > (
    SELECT CAST(SUM(Team_Attributes.buildUpPlayPassing) AS REAL) / COUNT(Team.team_long_name)
    FROM Team
    JOIN Team_Attributes
      ON Team.team_api_id = Team_Attributes.team_api_id
    WHERE Team_Attributes.buildUpPlayPassing IS NOT NULL
  );
```

### Explanation:
1. **`FROM Team JOIN Team_Attributes`**: Combines the team identities with their respective season-by-season performance metrics using their shared `team_api_id`.
2. **`WHERE strftime('%Y', Team_Attributes.date) = '2012'`**: Filters our list of teams to just those evaluated in the year 2012.
3. **`AND Team_Attributes.buildUpPlayPassing > (...)`**: Ensures that we are only returning teams whose passing score is strictly greater than the calculated global average.
4. **`SELECT CAST(SUM(...) AS REAL) / COUNT(...)`**: Calculates the precise average "build-up play passing" across the dataset, explicitly matching the division context provided in your request. The calculation also excludes records where 
there isn't a recorded score (`IS NOT NULL`).


