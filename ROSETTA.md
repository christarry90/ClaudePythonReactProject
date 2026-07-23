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
