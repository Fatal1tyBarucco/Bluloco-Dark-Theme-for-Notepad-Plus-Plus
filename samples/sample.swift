// Sample Swift code to test Bluloco Dark
// Includes Optionals, Closures, and Protocols

protocol Themeable {
    var name: String { get }
}

struct DarkTheme: Themeable {
    var name: String = "Bluloco Dark"
}

func applyTheme(theme: Themeable) {
    print("Applying \(theme.name)...")
}

let myTheme: Themeable? = DarkTheme()
if let theme = myTheme {
    applyTheme(theme: theme)
} else {
    print("No theme found")
}

let numbers = [1, 2, 3].map { $0 * 2 }
