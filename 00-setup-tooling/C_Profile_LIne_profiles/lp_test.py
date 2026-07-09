"""
_Profile_LIne_profiles  ↱ main ±  kernprof -l -v lp_test.py
Wrote profile results to 'lp_test.py.lprof'
Timer unit: 1e-06 s

Total time: 0 s
File: lp_test.py
Function: train_step at line 1

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     1                                           @profile
     2                                           def train_step(model, data, target):
     3                                               output = model(data)
     4                                               loss = F.cross_entropy(output, target)
     5                                               loss.backward()
     6                                               return loss

"""
@profile
def train_step(model, data, target):
    output = model(data)
    loss = F.cross_entropy(output, target)
    loss.backward()
    return loss

# Run with: kernprof -l -v lp_test.py