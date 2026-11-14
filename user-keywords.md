# USER KEYWORDS 1–8 — Suggested Keyword Lists

This document provides suggested keyword lists for the 8 USER KEYWORD slots available in Notepad++ Style Configurator for each supported lexer family. These slots map to the upstream VSCode Bluloco Dark `semanticTokenColors` roles and are **manual** — you must add the words yourself in Settings → Style Configurator → [Language] → User keywords.

## Slot Mapping (from upstream semanticTokenColors)

| Slot | Role | Color | Upstream Role |
|------|------|-------|---------------|
| 1 | Property | `#CE9887` | `property`, `member` |
| 2 | Constant | `#9F7EFE` | `constant`, `enumMember` |
| 3 | Parameter | `#8BCDEF` | `parameter`, `variable` |
| 4 | Function | `#3FC56B` | `function`, `method` |
| 5 | Decorator | `#50ACAE` | `decorator`, `annotation` |
| 6 | Namespace | `#FF839B` | `namespace`, `module` |
| 7 | Type Parameter | `#FF6480` | `typeParameter`, `type` |
| 8 | Macro | `#3FC56B` | `macro`, `keyword` (function-like) |

---

## C / C++ / C# / Java / JavaScript / TypeScript / PHP / ASP / Lua / GDScript

These 9 lexer families share the same USER KEYWORDS 1–8 slot assignments (styleIDs 128–135 or 200–207).

### Slot 1 — Property (`#CE9887`)
Object properties, struct/record fields, class members, JSON keys, CSS custom properties

```
prop property field member attribute key
this self Me thisptr base super
length size count capacity
name id value text label title
x y z width height top left right bottom
enabled visible active selected checked
```

### Slot 2 — Constant (`#9F7EFE`)
Enum members, constant values, readonly fields, define constants

```
TRUE FALSE NULL nil None nullptr undefined
MAX_MIN_VALUE MIN_VALUE MAX_VALUE
PI E PI_2 SQRT2
VERSION BUILD_DATE COMMIT_HASH
DEFAULT_CONFIG DEFAULT_OPTIONS
READ_WRITE READ_ONLY WRITE_ONLY
```

### Slot 3 — Parameter (`#8BCDEF`)
Function parameters, lambda parameters, template parameters

```
param arg argument p a b c d e f g h i j k
callback cb handler fn func
ctx context state env config opts options
req res request response next
err error e ex exception
self cls this that
```

### Slot 4 — Function (`#3FC56B`)
Function names, method names, callbacks, event handlers

```
init setup configure initialize
start stop run execute process handle
get set add remove delete update create destroy
load save parse serialize deserialize
validate check verify assert expect
onClick onChange onSubmit onLoad onError
callback handler listener emitter
map filter reduce forEach find some every
then catch finally await async
```

### Slot 5 — Decorator / Annotation (`#50ACAE`)
Decorators, attributes, annotations, metadata

```
@Component @Injectable @NgModule @Directive @Pipe
@Override @Deprecated @SuppressWarnings @Nullable @NonNull
@staticmethod @classmethod @property @abstract @override
@dataclass @field @validator @root_validator
@router.get @app.route @api.expect @jwt_required
@test @benchmark @ignore @skip @only
#[derive] #[cfg] #[async_trait] #[serde] #[tokio::main]
```

### Slot 6 — Namespace / Module (`#FF839B`)
Namespaces, modules, packages, imports

```
std stdio stdlib string vector map set
react react-dom next vue @vue/runtime-core
express mongoose axios lodash moment
System Collections Generic Linq Text
java.lang java.util java.io java.net
com.google.gson org.junit.jupiter.api
github.com/user/repo
```

### Slot 7 — Type Parameter / Type (`#FF6480`)
Generic type parameters, type aliases, interfaces, type names

```
T U V K V K E R
Key Value Element Item Result Error
Request Response Params Query Body
Props State Context Config Options
Callback Handler Listener Emitter
Promise Future Result Option Either
Map Set List Array Dict Tuple
```

### Slot 8 — Macro (`#3FC56B`)
Preprocessor macros, compile-time constants, function-like macros

```
DEBUG RELEASE NDEBUG
assert static_assert verify check
min max clamp abs sign
offsetof container_of ARRAY_SIZE
LOG_INFO LOG_WARN LOG_ERROR LOG_DEBUG
TODO FIXME NOTE HACK XXX
WIN32 LINUX MACOS ANDROID IOS
UNICODE _UNICODE WIN64 _WIN64
```

---

## Bash

USER KEYWORDS (styleID 12) — single slot, color `#CE9887` (Property)

```
# Common shell builtins and keywords not highlighted by default
local declare readonly export typeset
function select case in do done then else elif fi
time coproc
```

---

## Python

USER KEYWORDS 1–8 (styleIDs 128–135)

| Slot | Role | Suggested Keywords |
|------|------|-------------------|
| 1 | Property | `self cls this attr property field` |
| 2 | Constant | `True False None Ellipsis NotImplemented __name__ __file__` |
| 3 | Parameter | `args kwargs self cls *args **kwargs` |
| 4 | Function | `def lambda async def await yield from` |
| 5 | Decorator | `@property @staticmethod @classmethod @abstractmethod @dataclass @field @validator @root_validator @app.route @api.expect @jwt_required @pytest.fixture @pytest.mark.parametrize` |
| 6 | Namespace | `os sys json re math random datetime collections itertools functools typing pathlib` |
| 7 | Type | `List Dict Set Tuple Optional Union Any Callable TypeVar Generic Protocol TypedDict` |
| 8 | Macro | (N/A for Python — use for dunder methods) `__init__ __new__ __str__ __repr__ __eq__ __hash__ __len__ __getitem__ __setitem__ __enter__ __exit__ __call__ __iter__ __next__ __await__ __aenter__ __aexit__` |

---

## Rust (via C-family USER KEYWORDS)

If using C/C++ lexer for Rust, map slots to Rust semantics:

| Slot | Role | Suggested Keywords |
|------|------|-------------------|
| 1 | Property | `self field struct_field tuple_field` |
| 2 | Constant | `const static const_fn const_eval` |
| 3 | Parameter | `self mut self ref self box self` |
| 4 | Function | `fn async fn const fn unsafe fn extern fn` |
| 5 | Decorator | `#[derive] #[cfg] #[allow] #[warn] #[deny] #[inline] #[cold] #[test] #[bench] #[should_panic] #[ignore] #[doc] #[macro_export] #[proc_macro] #[proc_macro_derive] #[proc_macro_attribute]` |
| 6 | Namespace | `std core alloc collections hash sync thread time io fs net path ffi` |
| 7 | Type | `Option Result Vec HashMap HashSet Box Rc Arc Mutex RWLock RefCell Cell Pin Future Stream Iterator` |
| 8 | Macro | `macro_rules! format! println! vec! hashmap! try! await! select! join! spawn! main! test! bench! cfg! include! include_str! include_bytes! concat! stringify! file! line! column! module_path! env! option_env! cfg!` |

---

## How to Apply in Notepad++

1. Open **Settings → Style Configurator**
2. Select your language from the **Language** dropdown
3. In the **Style** list, find **USER KEYWORDS 1** through **USER KEYWORDS 8** (or **USER KEYWORDS** for Bash)
4. Click the style, then enter space-separated keywords in the **User-defined keywords** field
5. Click **Save & Close**

> **Tip:** Copy the keyword lists above into a text file, edit to match your project's conventions, then paste into the User-defined keywords field.

---

## Notes

- These are **suggestions only** — tailor them to your codebase, frameworks, and naming conventions
- USER KEYWORDS are **not semantic tokens** — they match exact words you provide, not AST nodes
- Keywords are case-sensitive in Notepad++
- Each lexer family has independent USER KEYWORD slots (C-family shares 128–135; JS/TS share 200–207; HTML has USER TAGS 192–195 and USER ATTRIBUTES 196–199; Lua has USER KEYWORDS 5–8 at 128–131)
- The color mapping follows the upstream Bluloco Dark `semanticTokenColors` for cross-editor consistency

---

*Generated for Bluloco Dark Theme for Notepad++ v2.2+*