require 'sqlite3'

class ProgMapper
  def initialize
    @db = SQLite3::Database.new "prog.db"
  end

  def average_qwr_by_year
    rows = db.execute <<-SQL
      SELECT year, AVG(qwr)
      FROM albums
      GROUP BY year
      ORDER BY year;
    SQL
  end

  private

  attr_reader :db
end
