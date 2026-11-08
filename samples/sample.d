// D sample — module, struct/class, functions, templates, strings, comments, UFCS.
// Targets the d lexer.

module sample;

// --- Comments ---
// Single-line comment.
/*
 Multi-line comment block.
 */

/** Doc comment. */
import std.stdio;
import std.string : format;

/// --- Struct and class ---
struct Point
{
    double x;
    double y;

    this(double x, double y)
    {
        this.x = x;
        this.y = y;
    }
}

class Shape
{
    string name;

    this(string name)
    {
        this.name = name;
    }

    void draw() const
    {
        writeln("Drawing ", name);
    }
}

/// --- Functions ---
double add(double a, double b)
{
    return a + b;
}

void printInfo(string msg)
{
    writeln("Info: ", msg);
}

/// --- Template ---
T max(T)(T a, T b)
{
    return (a > b) ? a : b;
}

/// --- UFCS (Uniform Function Call Syntax) ---
void main()
{
    auto p = Point(1.5, 2.5);
    auto s = Shape("Circle");

    // UFCS: p.to!string() style equivalent
    string coords = format!("(%s, %s)", p.x, p.y);
    writeln(coords);

    s.draw();

    // Strings and edge cases
    string normal = "hello";
    string raw = r"raw \n string";
    string hex = "\x41\x42\x43";
    wstring wide = w"wide string";
    dstring del = d"delimited string";

    auto best = max(10, 20);
    writeln("Best: ", best);
}
