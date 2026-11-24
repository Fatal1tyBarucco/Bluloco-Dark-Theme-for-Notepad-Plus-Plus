# USER KEYWORDS Guide — Bluloco Dark for Notepad++

## Overview

Bluloco Dark exposes **USER KEYWORDS 1–8** (or 1–5 for PHP) as semantic keyword slots that map directly to VSCode's `semanticTokenColors`. When you populate these lists in **Settings → Style Configurator**, your code gains semantic coloring beyond what the lexer provides automatically:

| Slot | Semantic Role | Color | Upstream `semanticTokenColors` |
|------|---------------|-------|-------------------------------|
| **1** | Property / Field | `CE9887` | `property`, `variable.property` |
| **2** | Constant / Enum | `9F7EFE` | `constant`, `enumMember` |
| **3** | Parameter | `8BCDEF` | `parameter`, `variable.parameter` |
| **4** | Function / Method | `3FC56B` | `function`, `method` |
| **5** | Decorator / Annotation | `50ACAE` | `decorator`, `annotation` |
| **6** | Namespace / Module | `FF839B` | `namespace`, `module` |
| **7** | Type Parameter / Generic | `FF6480` | `typeParameter`, `type.typeParameter` |
| **8** | Macro | `3FC56B` | `macro`, `keyword.macro` |

> **How it works:** Notepad++'s Scintilla lexers cannot semantically distinguish variables from function calls, or parameters from local variables. USER KEYWORDS are **manual keyword lists** — you tell the editor "these words are functions," "these are parameters," etc. The theme provides the color mapping; you provide the word lists.

---

## Quick Start

1. Open **Settings → Style Configurator**
2. Select **Bluloco Dark** from the theme dropdown
3. Pick a language (e.g., **C**, **Python**, **TypeScript**)
4. Find **USER KEYWORDS 1** through **USER KEYWORDS 8** in the style list
5. Click each, paste the corresponding list below into the "User-defined keywords" box
6. Click **Save & Close** → reopen your files

> **Tip:** Do this once per language you use. The lists persist in Notepad++'s `stylers.xml`.

---

## Per-Language Keyword Lists

### C / C++ / C# / Java / Go / RC / ActionScript / Swift / GDScript
*(USER KEYWORDS 1–8, styleIDs 128–135, `substyle1–8`)*

**USER KEYWORDS 1 — Properties/Fields (`CE9887`)**
```text
width height length size count capacity offset position x y z r g b a
top left right bottom margin padding border radius opacity visible
enabled disabled selected checked focused hovered pressed active
value text label title name id class style data src href alt
```

**USER KEYWORDS 2 — Constants/Enums (`9F7EFE`)**
```text
MAX MIN DEFAULT NULL TRUE FALSE TRUE FALSE YES NO ON OFF
PI E INFINITY NAN EPSILON VERSION BUILD DEBUG RELEASE
```

**USER KEYWORDS 3 — Parameters (`8BCDEF`)**
```text
callback handler listener emitter observer subscriber publisher
config options settings params args kwargs props attributes
self this that me _super base parent root owner target source
```

**USER KEYWORDS 4 — Functions/Methods (`3FC56B`)**
```text
init setup configure build create make new alloc initWith
start stop run execute process handle dispatch trigger emit
get set add remove insert delete update refresh reload sync
load save parse serialize deserialize encode decode format
validate check verify assert expect ensure require guard
find search filter map reduce forEach every some includes
sort reverse slice splice push pop shift unshift concat
```

**USER KEYWORDS 5 — Decorators/Annotations (`50ACAE`)**
```text
override deprecated experimental internal public private protected
static const final abstract virtual sealed async await
getter setter property computed observable inject singleton
```

**USER KEYWORDS 6 — Namespaces/Modules (`FF839B`)**
```text
std boost folly absl goog glib qt wx gtk sdl vulkan opengl
core foundation uikit appkit webkit blink v8 dart flutter
react redux mobx rxjs lodash ramda fp tslib
```

**USER KEYWORDS 7 — Type Parameters/Generics (`FF6480`)**
```text
T U V K V K2 V2 TKey TValue TElement TItem TResult TError
TRequest TResponse TData TPayload TConfig TOptions TState
```

**USER KEYWORDS 8 — Macros (`3FC56B`)**
```text
TODO FIXME HACK NOTE BUG XXX OPTIMIZE REFACTOR DEBUG_ASSERT
assert verify assume unreachable unimplemented todo fixme
```

---

### Python
*(USER KEYWORDS 1–8, styleIDs 128–135, `substyle1–8` + DECORATOR styleID 15 + ATTRIBUTE styleID 20 + BUILTINS styleID 19)*

**USER KEYWORDS 1 — Properties/Fields (`CE9887`)**
```text
self.__dict__ self._cache self._data self._config self._state
cls.__name__ cls.__module__ cls.__bases__ cls.__dict__
```

**USER KEYWORDS 2 — Constants/Enums (`9F7EFE`)**
```text
True False None Ellipsis NotImplemented __debug__
PI E TAU INF NAN MAXSIZE MAXUNICODE
```

**USER KEYWORDS 3 — Parameters (`8BCDEF`)**
```text
self cls *args **kwargs callback handler fn func callable
request response context session transaction connection
```

**USER KEYWORDS 4 — Functions/Methods (`3FC56B`)**
```text
__init__ __new__ __call__ __getitem__ __setitem__ __delitem__
__iter__ __next__ __enter__ __exit__ __str__ __repr__
__len__ __bool__ __eq__ __hash__ __getattr__ __setattr__
property classmethod staticmethod abstractmethod cached_property
async def await yield from import as try except finally
```

**USER KEYWORDS 5 — Decorators (`50ACAE`)**
```text
@dataclass @property @classmethod @staticmethod @abstractmethod
@cached_property @lru_cache @singledispatch @overload @final
@dataclass @field @validator @root_validator @model_validator
@router.get @router.post @app.route @blueprint.route
@pytest.fixture @pytest.mark @mock @patch @freeze_time
```

**USER KEYWORDS 6 — Namespaces/Modules (`FF839B`)**
```text
os sys pathlib json re datetime decimal fractions itertools
collections functools operator typing dataclasses enum abc
asyncio concurrent multiprocessing threading queue contextlib
numpy pandas matplotlib scipy sklearn torch tensorflow jax
requests httpx aiohttp flask django fastapi starlette pydantic
sqlalchemy alembic redis celery rq dramatiq
```

**USER KEYWORDS 7 — Type Parameters (`FF6480`)**
```text
T KT VT KT VT_co VT_contra T_co T_contra Any Optional Union
List Dict Set Tuple Sequence Mapping Iterable Iterator Generator
Callable Awaitable Coroutine TypeVar Generic Protocol TypedDict
```

**USER KEYWORDS 8 — Macros (`3FC56B`)**
```text
TODO FIXME HACK NOTE BUG XXX DEBUG type: ignore noqa pragma
```

---

### JavaScript / JavaScript (embedded) / TypeScript
*(JS/TS: USER KEYWORDS 1–8, styleIDs 200–207; TypeScript also has WINDOW INSTRUCTION styleID 19 + STRING RAW styleID 20)*

**USER KEYWORDS 1 — Properties/Fields (`CE9887`)**
```text
length size width height offsetTop offsetLeft clientWidth clientHeight
scrollTop scrollLeft innerWidth innerHeight outerWidth outerHeight
dataset attributes classList style parentNode nextSibling previousSibling
firstChild lastChild childNodes children textContent innerText
value checked disabled selected readonly required multiple
href src alt title rel target download media type name id class
```

**USER KEYWORDS 2 — Constants/Enums (`9F7EFE`)**
```text
Infinity NaN undefined null globalThis window document navigator
console Math JSON Reflect Symbol Proxy Promise Map Set WeakMap
Array Object Function String Number Boolean Date RegExp Error
```

**USER KEYWORDS 3 — Parameters (`8BCDEF`)**
```text
event e evt callback cb next done resolve reject fn handler
req res next context ctx state props params query body headers
dispatch getState subscribe unsubscribe observe next error complete
```

**USER KEYWORDS 4 — Functions/Methods (`3FC56B`)**
```text
then catch finally map filter reduce forEach find findIndex
some every includes indexOf lastIndexOf push pop shift unshift
splice slice concat join split trim replace match search
fetch axios request get post put patch delete head options
useState useEffect useContext useRef useMemo useCallback useReducer
createContext createRef forwardRef memo lazy Suspense
```

**USER KEYWORDS 5 — Decorators/Annotations (`50ACAE`)**
```text
@observable @computed @action @inject @singleton @provide @consume
@router.get @router.post @controller @middleware @guard @pipe
@Input @Output @ViewChild @ContentChild @HostListener @HostBinding
@Component @Directive @Pipe @Injectable @NgModule @NgComponent
```

**USER KEYWORDS 6 — Namespaces/Modules (`FF839B`)**
```text
react react-dom react-router redux mobx rxjs lodash ramda
vue vuex vue-router pinia nuxt next express koa fastify
jest vitest testing-library cypress playwright
webpack vite rollup esbuild swc babel typescript
```

**USER KEYWORDS 7 — Type Parameters/Generics (`FF6480`)**
```text
T K V TKey TValue TElement TItem TResult TError TRequest TResponse
Props State Context Ref Element Component Instance DefaultProps
InferType ReturnType Parameters ConstructorParameters InstanceType
```

**USER KEYWORDS 8 — Macros (`3FC56B`)**
```text
TODO FIXME HACK NOTE BUG XXX DEBUG @ts-ignore @ts-expect-error
```

---

### PHP
*(USER KEYWORDS 1–5, styleIDs 208–212, `substyle1–5`)*

**USER KEYWORDS 1 — Properties/Fields (`CE9887`)**
```text
$this-> $this->_ $this->get $this->set $this->has $this->is
$obj->property $obj->field $obj->attribute $model->column
```

**USER KEYWORDS 2 — Constants/Enums (`9F7EFE`)**
```text
PHP_VERSION PHP_OS PHP_INT_MAX PHP_FLOAT_MAX M_PI M_E
self::CLASS_CONSTANT ParentClass::CONSTANT Enum::CASE
```

**USER KEYWORDS 3 — Parameters (`8BCDEF`)**
```text
$request $response $params $args $options $config $data $entity
$callback $handler $listener $emitter $observer $next
```

**USER KEYWORDS 4 — Functions/Methods (`3FC56B`)**
```text
__construct __destruct __call __callStatic __get __set __isset
__unset __sleep __wakeup __serialize __unserialize __toString
__invoke __clone __debugInfo __set_state
```

**USER KEYWORDS 5 — Decorators/Annotations (`50ACAE`)**
```text
@Route @Entity @Table @Column @Id @GeneratedValue @OneToOne
@OneToMany @ManyToOne @ManyToMany @JoinColumn @JoinTable
@Attribute @Property @Method @Param @Return @Throws @Deprecated
```

---

### ASP
*(USER KEYWORDS 1–8, styleIDs 216–223)*

Same lists as C/C++/C# above — ASP uses the same lexer family.

---

### Lua
*(USER KEYWORDS 1–4 styleIDs 16–19 + USER KEYWORDS 5–8 styleIDs 128–131)*

**USER KEYWORDS 1–4 (styleIDs 16–19) — Properties/Fields/Constants/Parameters**
```text
self.this self.that obj.field obj.property obj.method
config.options settings.params constants.values
```

**USER KEYWORDS 5–8 (styleIDs 128–131) — Functions/Decorators/Namespaces/Types**
```text
vim.api.nvim_ require import module package
@class @field @param @return @generic @async
love.graphics love.audio love.filesystem love.system
```

---

### Bash
*(USER KEYWORDS 1–4 styleIDs 128–131 + USER SCALAR 1–4 styleIDs 132–135)*

**USER KEYWORDS 1–4 (`CE9887`, `9F7EFE`, `8BCDEF`, `3FC56B`)**
```text
$HOME $USER $PATH $PWD $OLDPWD $SHELL $TERM $LANG
$_ $? $! $$ $# $@ $* $- $$ $BASHPID $EUID $PPID
```

**USER SCALAR 1–4 (styleIDs 132–135) — Additional semantic slots**
```text
readonly local declare export alias unalias function
source . exec eval trap shift set unset
```

---

### PowerShell
*(USER KEYWORDS styleID 12 among other styles)*

**USER KEYWORDS (`3FC56B`)**
```text
$PSVersionTable $PSScriptRoot $PWD $HOME $env:PATH $env:USER
Get-ChildItem Get-Item Get-Content Set-Content Add-Content
Where-Object ForEach-Object Select-Object Sort-Object Group-Object
Measure-Object Compare-Object Tee-Object Out-File Out-String
Invoke-Expression Invoke-Command Invoke-WebRequest Invoke-RestMethod
```

---

## How to Apply (Step by Step)

### In Notepad++ Style Configurator:

1. **Settings** → **Style Configurator...**
2. **Select theme:** Bluloco Dark
3. **Language:** Choose your language (e.g., "C", "Python", "TypeScript")
4. **Style:** Scroll to **USER KEYWORDS 1** (or "User keywords 1")
5. **User-defined keywords box:** Paste the list for that slot
6. Repeat for USER KEYWORDS 2–8
7. **Save & Close**

### Bulk Import (Advanced)

Notepad++ stores user keywords in `%APPDATA%\Notepad++\stylers.xml`. You can edit this file directly:

```xml
<LexerType name="cpp" ...>
    <WordsStyle name="USER KEYWORDS 1" ... keywordClass="substyle1">
        <Keywords>width height length size count ...</Keywords>
    </WordsStyle>
    ...
</LexerType>
```

> **Backup `stylers.xml` before editing manually.**

---

## Verification

Open a file in the configured language. You should see:

- **Properties/fields** → brownish `CE9887`
- **Constants/enums** → purple `9F7EFE`
- **Parameters** → cyan `8BCDEF`
- **Function calls** → green `3FC56B`
- **Decorators** → teal `50ACAE`
- **Namespaces** → pink `FF839B`
- **Type parameters** → red-pink `FF6480`
- **Macros** → green `3FC56B`

If colors don't appear: verify the language is using the correct lexer (bottom-right status bar in Notepad++ shows current lexer).

---

## Customization

These lists are **starting points**. Customize for your codebase:

- Add your project's common property names (e.g., `user_id`, `account_balance`)
- Add your team's naming conventions (`handleClick`, `fetchData`, `validateInput`)
- Add framework-specific decorators (`@Component`, `@Injectable`, `@Entity`)
- Add your domain constants (`MAX_RETRY`, `DEFAULT_TIMEOUT`, `API_VERSION`)

The theme gives you the semantic color system; you give it the vocabulary.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Keywords not coloring | Check lexer name in status bar matches the one you configured |
| Case sensitivity | Notepad++ USER KEYWORDS are case-sensitive; add both `CamelCase` and `camelCase` if needed |
| Overlapping keywords | Later slots win; order: 1→8. Put most specific in higher slots |
| Reset to defaults | Delete the `<Keywords>` blocks for USER KEYWORDS in `stylers.xml` |
| PHP only has 1–5 | PHP lexer only exposes 5 user keyword slots in Notepad++ |

---

## Reference

- **Upstream semantic tokens:** [uloco/theme-bluloco-dark](https://github.com/uloco/theme-bluloco-dark) → `themes/bluloco-dark-color-theme.json` → `semanticTokenColors`
- **Notepad++ lexer model:** `tools/npp_lexer_model.json` (v8.9.9 `stylers.model.xml` inventory)
- **Theme XML:** `BlulocoDark.xml` → search for `USER KEYWORDS`

---

*Generated for Bluloco Dark v2.3.1+ — part of the onboarding experience to unlock the theme's full semantic coloring.*