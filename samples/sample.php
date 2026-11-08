<?php
/**
 * Sample PHP code to test Bluloco Dark.
 * Includes Namespaces, Arrays, and Heredoc.
 */
namespace App\Core;

class ThemeManager {
    private array $colors = ['bg' => '#282C34', 'fg' => '#ABB2BF'];

    public function render(): string {
        $name = "Bluloco";
        $html = <<<HTML
        <div class="theme">
            <h1>Welcome to {$name}</h1>
        </div>
        HTML;
        return $html;
    }
}

$manager = new ThemeManager();
echo $manager->render();
?>
