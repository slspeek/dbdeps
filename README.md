# DBDeps

An office database can grow quite complex as more features are added. Then it 
is nice to see how different database objects refer to one another. 
This comes in real handy if you want to see the impact of a considered refactoring.

## Requirements

Must have [graphviz](https://www.graphviz.org/) installed on your system.

## Usage

Press ALT-SHIFT-F10 with a database open. Or see the tools menu, for the
menuitem "Draw dependency graph".  

When you do so the tool creates a [graphviz](https://www.graphviz.org/) source file from 
the database objects from the open database. As it opens all forms and reports
for inspection the screen will flicker.
