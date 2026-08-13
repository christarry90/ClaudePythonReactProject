# ROSETTA — Java ↔ Python ↔ TypeScript

The tutor appends a row here after every lesson. This is your living cheat-sheet — and the
data source you'll render in the app's `/rosetta` panel in Milestone 5.

| Concept | Java | Python | TypeScript | Gotcha for a Java dev |
|---|---|---|---|---|
| Hash map | `HashMap<K,V>` | `dict` `{}` | `Record<K,V>` / `Map` | Python dict keys can be any hashable; no generics at runtime |
| List | `List<T>` / `ArrayList` | `list` `[]` | `T[]` / `Array<T>` | Python lists are heterogeneous; no `.add()` — use `.append()` |
| Set | `Set<T>` / `HashSet` | `set` `{ }` | `Set<T>` | `{}` alone is a dict, not a set — use `set()` for empty |
| Optional / null | `Optional<T>` / `null` | `T \| None` | `T \| null \| undefined` | `None` not `null`; check with `is None`, not `==` |
| Stream map/filter | `stream().map().filter()` | list comprehension | `.map().filter()` | `[x*2 for x in xs if x>0]` replaces the whole chain |
| POJO / record | `record Task(...)` | Pydantic `BaseModel` | `interface Task` | Pydantic validates at runtime; TS interface vanishes at runtime |
| Dependency injection | `@Autowired` | `Depends(...)` | (props / context) | FastAPI resolves `Depends` per-request |
| Interface | `interface Foo` | ABC / `Protocol` | `interface Foo` | Python duck-types; you often don't need an explicit interface |
| Equality | `.equals()` vs `==` | `==` vs `is` | `===` vs `==` | Python `==` = value, `is` = identity; JS: always prefer `===` |
| For-each loop | `for (T x : xs)` | `for x in xs:` | `for (const x of xs)` | Python blocks use indentation + `:`, no braces |
| Ternary | `c ? a : b` | `a if c else b` | `c ? a : b` | Python puts the condition in the middle |
| Print / log | `System.out.println` | `print()` | `console.log` | — |
| Route param binding | `@PathVariable`/`@RequestBody`/`@RequestParam` | inferred: name matches `{x}` in path → path param; Pydantic type → body; else → query param | route/query params (framework-dependent) | Inferred by name, not annotated — typo in param name silently becomes a query param, no compile error |
| HTTP error response | `ResponseStatusException` / `@ExceptionHandler` | `raise HTTPException(status_code=404, detail=...)` | `throw`/error boundary (framework-dependent) | Raise, don't return — FastAPI catches it and builds the JSON error response for you |
| UI tree construction | imperative `new Element(...)` / `appendChild` | n/a | JSX: `<App />` → `React.createElement(App, null)` | JSX isn't HTML in the browser — it's sugar for building a tree of plain objects (the "virtual DOM") that React reconciles against the real DOM |
| Non-null assertion | `Optional`/explicit null check | n/a | `value!` — "trust me, not null" | Zero runtime check, unlike Java's `Optional` — purely a compile-time promise; wrong guess = runtime crash |
| Component state | mutable field + manual UI update | n/a | `const [x, setX] = useState(init)` | Must call the setter to trigger a re-render — direct reassignment (`x = ...`) compiles fine but silently does nothing to the UI |
| Rendering booleans in JSX | `println`/concat always calls `.toString()` | n/a | `{cond}` renders nothing; `{String(cond)}` for text | React silently skips `true`/`false`/`null`/`undefined` in JSX — this is what makes `{cond && <Foo/>}` work, but it means `{someBoolean}` shows nothing unless you convert it yourself |
| List item identity | n/a (no direct equivalent — closest is `.equals()`/`.hashCode()` for collection identity) | n/a | `key={task.id}` on mapped JSX elements | `key` is a re-render diffing hint, not equality — using array index instead of a stable id breaks silently when the list is reordered/filtered |
| State update (functional form) | n/a | n/a | `setX((prev) => ...)` vs `setX(x + ...)` | Reading the state variable directly from closure can capture a stale value; the updater-function form always gets the true latest state — safer default habit |
| Controlled form input | n/a | n/a | `value={state}` + `onChange={(e) => setState(e.target.value)}` | Setting `value` without `onChange` makes the field effectively read-only — React expects the displayed value to always come from state, so you must round-trip it yourself |
