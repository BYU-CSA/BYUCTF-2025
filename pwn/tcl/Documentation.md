# Tiny Configuration Language (TCL) Documentation
This basic configuration language can be used for a variety of applications such as spinning up game servers, docker containers, etc. The basics of the language are described below. 

All TCL files must start with `#START` and end with `#END`. All data in between is in the format `key = value`. The spaces in between the key name and value is important. The key name can only be alphanumeric with underscores and can't start with a number. All values must be integers, floats, strings, or booleans. There are no restrictions on what the key names can be, it's simply up to the application you use it with to understand what the key signifies. All type enforcement for specific key values (like `port` must be an integer) is also performed by the application using the file and is not checked in this parser. This parser will only determine if the syntax is valid.

Example:
```
#START
debug = true
port = 8000
name = "myapp"
brightness = 8.0
#END
```

## Interacting with the Parser
To streamline checking multiple TCL files, you can validate multiple files with the same process. 

Type in your TCL file one line at a time, being sure to start with `#START` and end with `#END`. Once it receives an `#END`, it will let you know if the TCL file is valid or not, and you can start putting in another.