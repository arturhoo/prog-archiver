require 'sqlite3'

class ProgMapper
  def initialize
    db_path = File.join(File.dirname(__FILE__), '../db/prog.db')
    @db = SQLite3::Database.new db_path
  end

  def average_qwr_by_year
    db.execute <<-SQL
      SELECT year, AVG(qwr)
      FROM albums
      GROUP BY year
      ORDER BY year;
    SQL
  end

  def top_artists
    db.execute <<-SQL
      SELECT AVG(qwr), artists.name
      FROM albums
      INNER JOIN artists ON artist_id = artists.id
      GROUP BY artist_id
      HAVING COUNT(artist_id) >= 2
      ORDER BY AVG(qwr) DESC;
    SQL
  end

  def top_genres
    db.execute <<-SQL
      SELECT AVG(qwr), genre
      FROM albums
      GROUP BY genre
      ORDER BY AVG(qwr) DESC;
    SQL
  end

  private

  attr_reader :db
end
