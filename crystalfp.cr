require "yaml"
require "markdown"

# channel = Channel(Recipe).new
# recipes = [] of Recipe
# files.each do |f|
#   spawn {
#     channel.send Recipe.new(f)
#   }
#   recipes << channel.receive
# end

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
      "**#{z.first}** - *#{z.last}*"
    end
  end
  def ingredient_measure(measure) : String
    z = measure.split " "
    if measure.size == 1 || measure == "!"
      ""
    else
      if z.first.to_f > 1
        "#{z.first} #{expand_measure(z.last) + 's'} "
      else
        "#{z.first} #{expand_measure(z.last)} "
      end
    end
  end
  def expand_measure(measure)
    case measure
    when "c"
      "cup"
    when "t"
      "teaspoon"
    when "T"
      "tablespoon"
    when "ml"
      "milliliter"
    when "g"
      "gram"
    else
      measure
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
end

puts Recipe.new("./t.recipe").markdown
