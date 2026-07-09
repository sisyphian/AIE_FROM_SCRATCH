`cProfile`, `line_profiler`, `tracemalloc`, `memory_profiler`, `torch.cuda.memory_*` = profiling tools.

Different jobs.

* `cProfile` → Which functions slow?
* `line_profiler` → Which line inside function slow?
* `tracemalloc` → Which Python objects use RAM?
* `memory_profiler` → RAM change line-by-line.
* `torch.cuda.memory_*` → GPU VRAM usage.

---

# Why profiling?

Without profiling:

```
Program slow.

Guess:
- DataLoader?
- Model?
- Disk?
- Network?
- Python loop?
- NumPy?
- GPU?

No idea.
```

Profiling:

```
train()
    |
    +--- load_data()      2 sec
    |
    +--- augment()       18 sec
    |
    +--- model()          3 sec
```

Now fix right thing.

Never optimize blindly.

---

# cProfile

Built into Python.

Measures

* function calls
* total time
* cumulative time
* number calls

Command

```bash
python -m cProfile train.py
```

Common

```bash
python -m cProfile -s cumtime train.py
```

`-s`

Sort output.

Examples

```
time
cumtime
calls
name
```

Most useful

```
cumtime
```

because shows whole cost including child functions.

---

Example

```python
def preprocess():
    ...

def train():
    preprocess()
    forward()
    backward()

train()
```

Output

```
ncalls tottime percall cumtime percall function

1       0.10    0.10    12.00   12.00 train

1       8.20    8.20     8.20    8.20 preprocess

100     1.10    0.01     2.80    0.03 forward

100     0.80    0.01     1.00    0.01 backward
```

Meaning

```
train()
12 sec total

preprocess()
8.2 sec

forward()
2.8 sec

backward()
1 sec
```

Main bottleneck

```
preprocess()
```

---

## Columns

```
ncalls
```

Number calls.

```
500
```

called 500 times.

---

```
tottime
```

Time inside function only.

Does NOT include functions called inside.

Example

```
train()
{
    preprocess()
    model()
}
```

Suppose

```
train body
1 sec

preprocess
4 sec

model
5 sec
```

Then

```
tottime(train)=1
```

---

```
cumtime
```

Time including children.

```
cumtime(train)=10
```

because

```
1+4+5
```

---

Example

```python
def A():
    B()

def B():
    C()

def C():
    time.sleep(2)
```

Result

```
Function     tottime   cumtime

A             0.00      2.00
B             0.00      2.00
C             2.00      2.00
```

---

When use `cProfile`

Whole application.

Questions

```
Where time going?
Which function slow?
How many calls?
```

---

# line_profiler

Sometimes function huge.

```
train_step()
```

takes

```
8 sec
```

Need know WHICH LINE.

Use

```bash
pip install line_profiler
```

Decorate

```python
@profile
def train_step(model, data, target):
    output = model(data)
    loss = F.cross_entropy(output, target)
    loss.backward()
    return loss
```

Run

```bash
kernprof -l -v train.py
```

Output

```
Line     Time

12       2 ms
13      60 ms
14     420 ms
15       1 ms
```

Immediately know

```
loss.backward()
```

slowest line.

---

Another example

```python
@profile
def process(data):
    x = load(data)
    y = augment(x)
    z = normalize(y)
    return z
```

Output

```
load()       5%

augment()   80%

normalize() 15%
```

Need optimize

```
augment()
```

---

Difference

```
cProfile

Function level

-------------------

train()
load()
forward()
backward()
```

```
line_profiler

Line level

x = load()
y = preprocess()
loss.backward()
```

Much more detailed.

---

# tracemalloc

Tracks Python memory allocations.

CPU RAM only.

Not GPU.

Built into Python.

Start

```python
import tracemalloc

tracemalloc.start()
```

After code

```python
snapshot = tracemalloc.take_snapshot()
```

Analyze

```python
top_stats = snapshot.statistics("lineno")

for stat in top_stats[:10]:
    print(stat)
```

Output

```
main.py:52
120 MB

loader.py:19
80 MB

dataset.py:105
60 MB
```

Meaning

```
Line 52 allocated 120 MB.
```

Very useful memory leak hunting.

---

Example

```python
images = []

for i in range(100000):
    images.append(load_image())
```

Memory growing forever.

`tracemalloc`

```
main.py:8

850 MB
```

Need inspect line 8.

---

Statistics options

```
statistics("lineno")
```

Per line.

```
statistics("filename")
```

Per file.

```
statistics("traceback")
```

Full allocation stack.

---

Take two snapshots

```python
before = tracemalloc.take_snapshot()

run()

after = tracemalloc.take_snapshot()

stats = after.compare_to(before, "lineno")
```

Now see memory increase.

Excellent leak detection.

---

# memory_profiler

Simpler.

Shows RAM usage every line.

Install

```bash
pip install memory_profiler
```

Decorate

```python
from memory_profiler import profile

@profile
def load_data():
    raw = read_csv("data.csv")
    processed = preprocess(raw)
    return processed
```

Run

```bash
python -m memory_profiler script.py
```

Output

```
Line     Memory

10       55 MB

11      420 MB

12      610 MB

13      610 MB
```

Interpretation

```
Line 11

Loaded CSV

+365 MB
```

```
Line 12

Processing

+190 MB
```

Need optimize those lines.

---

Common use

```
Huge DataFrame

Huge NumPy array

Huge list

Huge dictionary
```

Need know where RAM explodes.

---

Difference

`tracemalloc`

* Python allocator
* snapshots
* compare snapshots
* leak detection
* allocation source

`memory_profiler`

* process RAM
* line-by-line
* easier read
* peak memory

---

# GPU profiling

CPU profiler cannot see GPU VRAM.

PyTorch provides APIs.

---

## memory_allocated()

```python
torch.cuda.memory_allocated()
```

Returns

Currently used tensor memory.

Example

```
2.4 GB
```

Meaning

Live tensors occupy 2.4 GB.

---

## memory_reserved()

```python
torch.cuda.memory_reserved()
```

PyTorch caching allocator.

Suppose

GPU

```
24 GB
```

Need

```
2 GB
```

PyTorch requests

```
4 GB
```

Uses

```
2 GB
```

Keeps

```
2 GB
```

for future allocations.

Then

```
Allocated
2 GB

Reserved
4 GB
```

Reserved ≥ Allocated.

---

Example

```python
print(torch.cuda.memory_allocated())
print(torch.cuda.memory_reserved())
```

Output

```
Allocated

6.1 GB

Reserved

8.3 GB
```

Meaning

```
6.1 GB
```

actively used.

```
2.2 GB
```

cached.

---

Why cache?

Without cache

```
Allocate

Free

Allocate

Free
```

GPU allocator slow.

Instead

```
Allocate

Keep

Reuse
```

Much faster.

---

## memory_summary()

```python
print(torch.cuda.memory_summary())
```

Prints report.

Example

```
Allocated memory

Active memory

Reserved memory

Peak memory

Allocation count

Largest block
```

Useful debugging

```
CUDA out of memory
```

or fragmentation.

---

Other useful APIs

Current peak

```python
torch.cuda.max_memory_allocated()
```

Peak reserved

```python
torch.cuda.max_memory_reserved()
```

Reset counters

```python
torch.cuda.reset_peak_memory_stats()
```

Empty cache

```python
torch.cuda.empty_cache()
```

Returns unused cached blocks to CUDA driver. Does not free memory still referenced by tensors.

---

# Which tool use?

| Goal                          | Tool                            |
| ----------------------------- | ------------------------------- |
| Find slow function            | `cProfile`                      |
| Find slow line                | `line_profiler`                 |
| Find Python allocation source | `tracemalloc`                   |
| Find RAM increase per line    | `memory_profiler`               |
| Check GPU VRAM                | `torch.cuda.memory_allocated()` |
| Full GPU memory report        | `torch.cuda.memory_summary()`   |

# Typical AI workflow

1. Program slow.
2. Run:

```bash
python -m cProfile -s cumtime train.py
```

3. Slow function found.
4. Add `@profile`.
5. Run:

```bash
kernprof -l -v train.py
```

6. Optimize slow lines.
7. If RAM grows unexpectedly:

```python
import tracemalloc
```

or

```python
from memory_profiler import profile
```

8. If GPU runs out of memory:

```python
print(torch.cuda.memory_summary())
print(torch.cuda.memory_allocated())
print(torch.cuda.memory_reserved())
```

Repeat after each optimization. Measure first, optimize second.
