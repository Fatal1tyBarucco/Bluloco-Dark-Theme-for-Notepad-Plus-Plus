# Sample Ruby code to test Bluloco Dark
# Includes blocks, symbols, and interpolation

class Theme
  attr_accessor :name

  def initialize(name)
    @name = name
  end

  def describe
    puts "Theme: #{@name}"
  end
end

themes = [:dark, :light, :contrast]
themes.each do |t|
  puts "Processing #{t}..."
end

Theme.new("Bluloco Dark").describe
