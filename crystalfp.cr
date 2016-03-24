require "yaml"
require "markdown"

def go(input : String, output : String)
  files = Dir.glob File.join(input,"*.recipe")
  channel = Channel(Recipe).new
  recipes = [] of Recipe
  files.each do |f|
    spawn {
      channel.send Recipe.new(f)
    }
    recipes << channel.receive
  end
  recipes.each do |r|
    puts r.name
  end
end

class Recipe
  def initialize(recipe_file)
    @markdown = [] of String
    @markdown << ""

    h = YAML.parse(File.read(recipe_file)).as_h
    @name = h.delete "name"
    process(h,2)
  end
  def add(e)
    @markdown << e.chomp "\n"
  end
  def header(s,d)
    padding
    add "#{"#"*d} #{s}"
    padding
  end
  def padding()
    add "" unless @markdown.last == ""
  end
  def process(h : Hash, d : Int)
    h.each do |k,v|
      if v.is_a? String && k.is_a? String
        process_ingredient k,v
      elsif v.is_a? Hash
        header k,d
        process v,d+1
      elsif v.is_a? Array
        header k,d
        process_instructions v
      end
    end
  end
  def process_ingredient(k : String, v : String)
    name = ingredient_name k
    measure = ingredient_measure v
    add "- #{measure + name}"
  end
  def ingredient_name(name : String) : String
    z = name.split " - "
    if z.size == 1
      "**#{z.first}**"
    else
      "**#{z.first}** *#{z.last}*"
    end
  end
  def ingredient_measure(measure) : String
    z = measure.split " "
    if z.size == 1 || measure == "!"
      ""
    else
      m_amount = z.first.to_f
      m_type = z.last
      "#{m_amount} #{expand_measure(m_type) + (m_amount > 1 ? "s " : " ")}"
    end
  end
  def expand_measure(measure)
    case measure
    when "c"; "cup"
    when "t"; "teaspoon"
    when "T"; "tablespoon"
    when "ml"; "milliliter"
    when "g"; "gram"
    else; measure
    end
  end
  def process_instructions(a : Array)
    padding
    a.each do |v|
      add v as String
      padding
    end
  end
  def html
    Markdown.to_html @markdown.join("\n")
  end
  def markdown
    @markdown.join "\n"
  end
  def name
    @name
  end
end

# puts Recipe.new("./t.recipe").name
go("../recipes",".")
