You can run `./run` to get a list of commands and each command has documentation in the run file itself.

It's a shell script that has a number of functions defined to help you interact with this project. It's basically a Makefile except with less limitations. For example as a shell script it allows us to pass any arguments to another program.

This comes in handy to run various Docker commands because sometimes these commands can be a bit long to type.

Here is a list of common commands:

### Lint the code

```
# You should get no output (that means everything is operational).
./run lint
```

### Sort Python Imports

```
# You should see that everything is unchanged (imports are already formatted).
./run format:imports
```

### Format the code

```
# You should see that everything is unchanged (it's all already formatted).
./run format
```

!!! tip

    You can also run `./run quality` command to run the above 3 commands together.

### Running Tests

```
# You should see all passing tests. Warnings are typically ok.
./run manage test
```
