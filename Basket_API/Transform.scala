
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types.{IntegerType,StringType,StructType,StructField}
import org.apache.spark.sql.functions.col 
import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.Column

object NBA{
  def main(args: Array[String]) {
    val spark = SparkSession
                  .builder()
                  .appName("Transform")
                  .getOrCreate()
   // val sub_temp = temp.filter(col("code_insee_region") === 24 || 
     //                         col("code_insee_region") === 28)
//DataFrame avec le nombre de points marqués par l'équipe, l'id du match, le nom et l'id de l'équipe. 

//{"id": 473358, "date": "2021-10-04T00:00:00.000Z", 
//"home_team": {"id": 2, "abbreviation": "BOS", "city": "Boston", "conference": "East", "division": "Atlantic", "full_name": "Boston Celtics", "name": "Celtics"}, 
//"home_team_score": 98, "period": 4, "postseason": false, "season": 2021, "status": "Final", "time": "", 
//"visitor_team": {"id": 22, "abbreviation": "ORL", "city": "Orlando", "conference": "East", "division": "Southeast", "full_name": "Orlando Magic", "name": "Magic"}, 
//"visitor_team_score": 97}, 

val games = spark.read
                   .option("inferSchema","true")
                  .option("multiline","true")
                  .json("data/games_exam.json")              
games.printSchema()
//games.show(false)
val games_df = games.select(col("data.id").alias("id_game"),
                            col("data.home_team.id").alias("home_team_id"),
                            col("data.home_team.full_name").alias("home_team_name"),
                            col("data.home_team_score").alias("home_team_score"),
                            col("data.visitor_team.id").alias("away_team_id"),
                            col("data.visitor_team.full_name").alias("away_team_name"),
                            col("data.visitor_team_score").alias("away_team_score"),
                            )
games_df.show(false)
val listTeams = Seq("Atlanta Hawks","Phoenix Suns","Milwaukee Bucks","LA Clippers")
//games_df.filter(! (games_df("home_team_name").isin(listTeams :_*) && games_df("away_team_name").isin(listTeams :_*))).select("home_team_name","away_team_name").show()
//games_df.filter("home_team_name IN ('Atlanta Hawks','Phoenix Suns','Milwaukee Bucks','LA Clippers') AND away_team_name IN ('Atlanta Hawks','Phoenix Suns','Milwaukee Bucks','LA Clippers')").show()
 val f = Seq(1,13,24,17)

//games_df.filter(games_df("home_team_id").isin(f  : _*)).show()
 
//withColumn permet de modifier les valeurs d'une colonne mais aussi de créer une colonne à l'instar des DataFrame de pandas.
 //renommer la colonne à l'aide de la fonction withColumnRenamed : 

 val stats = spark.read
                   .option("inferSchema","true")
                  .option("multiline","true")
                  .json("data/stats_exam.json")    

   val  stats_df = stats.withColumn("game_id",col("data.game.id"))
                        .withColumn("id_team",col("data.team.id"))
                        .withColumn("team_name",col("data.team.full_name"))
                          .select(
                                col("game_id"),
                                col("id_team"),
                                col("team_name"))
                                //col("data.ast").cast("int"),
                             //    col("data.blk").cast("float"),
                             //    col("data.dreb").cast("float"),
                           //     col("data.fg3_pct").cast("float"),
                             //   col("data.fg3m").cast("float"),
                              //   col("data.fg3a").cast("float"),
                              //   col("data.fg_pct").cast("float"),
                             //    col("data.fta").cast("float"),
                              //   col("data.ftm").cast("float"),
                             //   col("data.oreb").cast("float"),
                             //   col("data.pf").cast("float"),
                             //   col("data.pts").cast("float"),
                            //   col( "data.reb").cast("float"),
                             //  col( "data.stl")cast("float"))

                          
                      //  .drop("data.game","data.player","data.min","data.team.","data.meta")
//.select( Seq("game_id","id_team","team_name","data.ast","data.blk","data.dreb","data.fg3_pct","data.fg3m","data.fg3a","data.fg_pct","data.fta",
  //"data.ftm","data.oreb","data.pf","data.pts","data.reb","data.stl").map(m=>col(m).cast("float")):_*)
stats_df.printSchema()
// groupez les lignes par l'équipe et l'id du match. 
//val exprs = df.columns.map((_ -> "mean")).toMap
//df.groupBy($"col1").agg(exprs).show()
val exprs = stats_df.columns.map((_ -> "mean")).toMap
//val col_agg =Seq("ast","blk","dreb","fg3","fg3m","fg3a","fg_pct","fta","ftm","oreb","pf","pts","reb","stl")
val col_agg =Seq("pts")
val  stats_group_by:DataFrame= stats_df//.groupBy("game_id","id_team","team_name")//.sum(col_agg.map(x=>"data."+x):_*)//.avg(col_agg.map(x=>"data."+x):_*)//.as(col_agg.map(_+"_AVG"):_*)
                    //     .agg(
                     //  exprs
  //)//.withColumnRenamed(stats_group_by.drop("id_game","id_team","team_name").columns :_*,
     //                   stats_group_by.drop("id_game","id_team","team_name").columns.map(_.take(4)) :_*)

val df_fusion = stats_group_by.join(games_df,(games_df("id_game") === stats_group_by("game_id")) 
                                    and ((games_df("home_team_id")=== stats_group_by("id_team"))     or (games_df("away_team_id") === stats_group_by("id_team")) )
                                   and ((games_df("home_team_name") === stats_group_by("team_name")) or (games_df("away_team_name") === stats_group_by("team_name"))))
                          //.groupBy("id_game","id_team","team_name").sum(col_agg.map(x=>"data."+x):_*)//.avg(col_agg.map(x=>"data."+x):_*)//.as(col_agg.map(_+"_AVG"):_*)
//("workExperience", col("workExperience").cast("string"))
 df_fusion.write.format("csv").option("header","true").save("data/df_final")                   
  }
}

// spark-submit  --class NBA  --master local[2]

//spark-submit --class "NBA" --master local[2] target/scala-2.12/nba_2.12-1.0.jar
  //--deploy-mode <deploy-mode> \
  //--conf <key>=<value> \

  /*
  root
 |-- data: array (nullable = true)
 |    |-- element: struct (containsNull = true)
 |    |    |-- date: string (nullable = true)
 |    |    |-- home_team: struct (nullable = true)
 |    |    |    |-- abbreviation: string (nullable = true)
 |    |    |    |-- city: string (nullable = true)
 |    |    |    |-- conference: string (nullable = true)
 |    |    |    |-- division: string (nullable = true)
 |    |    |    |-- full_name: string (nullable = true)
 |    |    |    |-- id: long (nullable = true)
 |    |    |    |-- name: string (nullable = true)
 |    |    |-- home_team_score: long (nullable = true)
 |    |    |-- id: long (nullable = true)
 |    |    |-- period: long (nullable = true)
 |    |    |-- postseason: boolean (nullable = true)
 |    |    |-- season: long (nullable = true)
 |    |    |-- status: string (nullable = true)
 |    |    |-- time: string (nullable = true)
 |    |    |-- visitor_team: struct (nullable = true)
 |    |    |    |-- abbreviation: string (nullable = true)
 |    |    |    |-- city: string (nullable = true)
 |    |    |    |-- conference: string (nullable = true)
 |    |    |    |-- division: string (nullable = true)
 |    |    |    |-- full_name: string (nullable = true)
 |    |    |    |-- id: long (nullable = true)
 |    |    |    |-- name: string (nullable = true)
 |    |    |-- visitor_team_score: long (nullable = true)
 |-- meta: struct (nullable = true)
 |    |-- current_page: long (nullable = true)
 |    |-- next_page: long (nullable = true)
 |    |-- per_page: long (nullable = true)
 |    |-- total_count: long (nullable = true)
 |    |-- total_pages: long (nullable = true)
 */ 
