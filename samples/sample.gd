# GDScript sample — extends, class_name, func, signals, annotations, node paths, strings.
# Targets the gdscript lexer.

# --- Comments ---
# Single-line comment.
"""Multi-line docstring comment."""

# --- Class and annotations ---
extends Node2D
class_name Player

@export var speed: float = 100.0
@export var health: int = 100
@onready var sprite: Sprite2D = $Sprite2D

# --- Signals ---
signal health_changed(new_health: int)
signal player_died

# --- Variables ---
var position: Vector2 = Vector2.ZERO
var name: String = "Player"
var is_alive: bool = true

# --- Constants ---
const MAX_SPEED: float = 500.0
const GRAVITY: float = 9.8

# --- Functions ---
func _ready() -> void:
    print("Player ready")
    _process.connect("health_changed", self, "_on_health_changed")

func _process(delta: float) -> void:
    var input = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    position += input * speed * delta
    $Sprite2D.position = position

func take_damage(amount: int) -> void:
    health -= amount
    health_changed.emit(health)
    if health <= 0:
        die()

func die() -> void:
    player_died.emit()
    queue_free()

# --- Private function (underscore prefix) ---
func _on_health_changed(new_health: int) -> void:
    print("Health is now: ", new_health)

# --- Edge cases: strings, node paths, arrays, dictionaries, enum ---
var message: String = "Hello, Godot!"
var raw_string: String = r"raw \n string"
var triple: String = """Triple-quoted
string"""

var items: Array = [1, 2, 3]
var data: Dictionary = {"key": "value", "number": 42}

enum {STATE_IDLE, STATE_RUNNING, STATE_JUMPING}

var node_path: NodePath = "Player/Sprite2D"
var callable: Callable = callable(_process, 1.0)
