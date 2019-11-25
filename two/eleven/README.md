# Problem 2.11
Build a vacuum cleaning agent for arbitrary and unknown map dimensions

```
python two_eleven.py
```

I present 3 agents that attempt to solve the problem
- simple_reflex: uses condition-action rules with no concept of the state of the map
- random_relfex: randomly chooses between up,down,left, right. Always cleans if it is above a dirty square
- rational_reflex: optimally with respect to number of squares cleans the unknown map. Its optimality is
discussed in the attached pdf