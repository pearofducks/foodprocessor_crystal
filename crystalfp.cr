require "yaml"
require "markdown"

class Recipe
  def initialize(recipe_file)
    @markdown = [] of String
    h = YAML.parse(File.read(recipe_file)).as_h
    @name = h.delete "name"
    puts @name
    process(h,2)
  end
  def header(s,d)
    @markdown << "#{"#"*d}#{s}"
  end
  def process(h,d)
    h.each do |k,v|
      # we need to check both k and v, otherwise methods in
      # process_ingredients complain
      if v.is_a?(String)
        process_ingredient(k as String,v)
      elsif v.is_a?(Hash)
        header(k,d)
        process(v,d+1)
      elsif v.is_a?(Array)
        header(k,d)
        process_instructions(v)
      end
    end
  end
  def process_ingredient(k,v)
    name = ingredient_name(k)
    measure = ingredient_measure(v)
  end
  def ingredient_name(name)
    z = name.split(" - ")
    if z.size == 1
      z.first
    else
      "#{z.first} - *#{z.last}*"
    end
  end
  def ingredient_measure(measure)
                # 'c': 'cup',
                # 't': 'teaspoon',
                # 'T': 'tablespoon',
                # 'ml': 'milliliter',
                # 'g': 'gram',
                # 'p': False
  end
  def process_instructions(a)
    a.each do |v|
      puts v
    end
  end
  def html
    Markdown.to_html(@markdown)
  end
end

puts Recipe.new("./t.recipe").html
