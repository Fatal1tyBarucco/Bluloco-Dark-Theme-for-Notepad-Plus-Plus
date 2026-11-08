# Sample C# code to test Bluloco Dark
using System;
using System.Collections.Generic;
using System.Linq;

namespace BlulocoSample {
    /// <summary>
    /// Tests LINQ, generics, and string interpolation
    /// </summary>
    public class Program {
        public static void Main(string[] args) {
            var list = new List<int> { 1, 2, 3, 4, 5 };
            var evens = list.Where(x => x % 2 == 0).ToList();
            
            string name = "Developer";
            Console.WriteLine($"Hello {name}, you found {evens.Count} even numbers.");
        }
    }
}
